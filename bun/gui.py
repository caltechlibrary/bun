'''
gui.py: graphical user interface class for Bun

Explanation of the architecture
-------------------------------

After trying alternatives and failing to get things to work, I settled on the
following approach that works on both Mac and Windows 10 in my testing.

The control flow of this program is somewhat inverted from a typical WxPython
application.  The typical application would be purely event-driven: it would
be implemented as an object derived from wx.Frame with methods for different
kinds of actions that the user can trigger by interacting with controls in
the GUI.  Once the WxPython app.MainLoop() function is called, nothing
happens until the user does something to trigger an activitiy.  Conversely,
in this program, I not only wanted to allow command-line based interaction,
but also wanted the entire process to be started as soon as the user starts
the application.  This is incompatible with the typical event-driven
application structure because there's an explicit sequential driver and it
needs to be kicked off automatically after app.MainLoop() is called.

The approach taken here has two main features.

* First, there are two threads running: one for the WxPython GUI MainLoop()
  code and all GUI objects (like AppFrame and UserDialog in this file), and
  another thread for the real main body that implements the program's sequence
  of operations.  The main thread is kicked off by the GUI class start()
  method right before calling app.MainLoop().

* Second, the main body thread invokes GUI operations using a combination of
  in-application message passing (using a publish-and-subscribe scheme from
  PyPubsub) and the use of wx.CallAfter().  The AppFrame objects implement
  some methods that can be invoked by other classes, and AppFrame defines
  subscriptions for messages to invoke those methods.  Callers then have to
  use the following idiom to invoke the methods:

    wx.CallAfter(pub.sendMessage, "name", arg1 = "value1", arg2 = "value2")

  The need for this steps from the fact that in WxPython, if you attempt to
  invoke a GUI method from outside the main thread, it will either generate
  an exception or (what I often saw on Windows) simply hang the application.
  wx.CallAfter places the execution into the thread that's running
  MainLoop(), thus solving the problem.

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2019-2020 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

import os
import os.path as path
from   pubsub import pub
from   queue import Queue
import wx
import wx.adv
import wx.lib
from   wx.lib.dialogs import ScrolledMessageDialog
import wx.richtext
import sys

if __debug__:
    from sidetrack import set_debug, log, logr

from .base import UIBase
from .app_frame import AppFrame


# Exported classes.
# .............................................................................

class GUI(UIBase):
    '''Graphical user interface.'''

    def __init__(self, name, subtitle, show_banner, use_gui, use_color, be_quiet):
        super().__init__(name, subtitle, show_banner, use_gui, use_color, be_quiet)

        # Initialize our main GUI window.
        self._app = wx.App()
        self._frame = AppFrame(name, subtitle, None, wx.ID_ANY)
        self._app.SetTopWindow(self._frame)
        self._frame.Center()
        self._frame.Show(True)

        # Initialize some stuff we use to communicate with dialogs.
        self._queue = Queue()
        self._response = None


    def start(self):
        '''Start the user interface.'''
        if __debug__: log('starting main UI loop')
        self._app.MainLoop()


    def stop(self):
        '''Stop the user interface.'''
        if __debug__: log('stopping UI')
        wx.CallAfter(self._frame.Destroy)


    def confirm(self, question):
        '''Asks the user a yes/no question using a GUI dialog.'''
        if __debug__: log('generating yes/no dialog')
        wx.CallAfter(self._ask_yes_no, question)
        self._wait()
        if __debug__: log('got response: {}', self._response)
        return self._response


    def login_details(self, prompt, user = None, password = None):
        '''Shows a login-and-password dialog, and returns a tuple of user,
        password, and a Boolean indicating whether the user cancelled the
        dialog.  The dialog will be filled in with the values of 'user' and/or
        'password', if they are provided.
        '''
        # This uses a threadsafe queue to implement a semaphore.  The
        # login_dialog will put a results tuple on the queue, but until then,
        # a get() on the queue will block.  Thus, this function will block
        # until the login dialog is closed by the user.
        results = Queue()
        if __debug__: log('sending message to login_dialog')
        wx.CallAfter(pub.sendMessage, "login_dialog", results = results,
                     user = user, password = password)
        if __debug__: log('blocking to get results')
        results_tuple = results.get()
        if __debug__: log('name_and_password results obtained')
        # Results will be a tuple of user, password, cancelled
        return results_tuple[0], results_tuple[1], results_tuple[2]


    def file_selection(self, type, message, pattern):
        return_queue = Queue()
        if __debug__: log(f'sending message to {type} file')
        if type == 'open':
            wx.CallAfter(pub.sendMessage, 'open_file', return_queue = return_queue,
                         message = message, pattern = pattern)
        else:
            wx.CallAfter(pub.sendMessage, 'save_file', return_queue = return_queue,
                         message = message)
        if __debug__: log('blocking to get results')
        return_queue = return_queue.get()
        if __debug__: log('got results')
        return return_queue


    def inform(self, text, *args):
        '''Print an informational message.'''
        if __debug__: log('generating info notice')
        wx.CallAfter(pub.sendMessage, "info_message", message = text.format(*args))


    def warn(self, text, *args):
        '''Print a nonfatal, noncritical warning message.'''
        if __debug__: log('generating warning notice')
        wx.CallAfter(pub.sendMessage, "info_message",
                     message = 'Warning: ' + text.format(*args))


    def alert(self, text, *args, **kwargs):
        '''Print a message reporting a critical error.'''
        if __debug__: log('generating error notice')
        message = text.format(*args)
        details = kwargs['details'] if 'details' in kwargs else ''
        if wx.GetApp().TopWindow:
            wx.CallAfter(self._show_alert_dialog, message, details, 'error')
        else:
            # The app window is gone, so wx.CallAfter won't work.
            self._show_alert_dialog(message, details, 'error')
        self._wait()


    def alert_fatal(self, text, *args, **kwargs):
        '''Print a message reporting a fatal error.  The keyword argument
        'details' can be supplied to pass a longer explanation that will be
        displayed if the user presses the 'Help' button in the dialog.

        When the user clicks on 'OK', this causes the UI to quit.  It should
        result in the application to shut down and exit.
        '''
        if __debug__: log('generating fatal error notice')
        message = text.format(*args)
        details = kwargs['details'] if 'details' in kwargs else ''
        if wx.GetApp().TopWindow:
            wx.CallAfter(self._show_alert_dialog, message, details, 'fatal')
        else:
            # The app window is gone, so wx.CallAfter won't work.
            self._show_alert_dialog(message, details, 'fatal')
        self._wait()
        wx.CallAfter(pub.sendMessage, 'stop')


    def _ask_yes_no(self, question):
        '''Display a yes/no dialog.'''
        frame = self._current_frame()
        dlg = wx.GenericMessageDialog(frame, question, caption = self._name,
                                      style = wx.YES_NO | wx.ICON_QUESTION)
        clicked = dlg.ShowModal()
        dlg.Destroy()
        frame.Destroy()
        self._response = (clicked == wx.ID_YES)
        self._queue.put(True)


    def _show_note(self, text, *args, severity = 'info'):
        '''Displays a simple notice with a single OK button.'''
        if __debug__: log('showing note dialog')
        frame = self._current_frame()
        icon = wx.ICON_WARNING if severity == 'warn' else wx.ICON_INFORMATION
        dlg = wx.GenericMessageDialog(frame, text.format(*args),
                                      caption = self._name, style = wx.OK | icon)
        clicked = dlg.ShowModal()
        dlg.Destroy()
        frame.Destroy()
        self._queue.put(True)


    def _show_alert_dialog(self, text, details, severity = 'error'):
        if __debug__: log('showing message dialog')
        frame = self._current_frame()
        if severity == 'fatal':
            short = text
            style = wx.OK | wx.ICON_ERROR
            extra_text = 'fatal '
        else:
            short = text + '\n\nWould you like to try to continue?\n(Click "no" to quit now.)'
            style = wx.YES_NO | wx.YES_DEFAULT | wx.ICON_EXCLAMATION
            extra_text = ''
        if details:
            style |= wx.HELP
        caption = self._name + f" has encountered a {extra_text}problem"
        dlg = wx.MessageDialog(frame, message = short, style = style, caption = caption)
        clicked = dlg.ShowModal()
        if clicked == wx.ID_HELP:
            body = (self._name + " has encountered a problem:\n"
                    + "─"*30
                    + "\n{}\n".format(details or text)
                    + "─"*30
                    + "\nIf the problem is due to a network timeout or "
                    + "similar transient error, then please quit and try again "
                    + "later. If you don't know why the error occurred or "
                    + "if it is beyond your control, please also notify the "
                    + "developers.\n")
            info = ScrolledMessageDialog(frame, body, "Error")
            info.ShowModal()
            info.Destroy()
            frame.Destroy()
            self._queue.put(True)
            if 'fatal' in severity:
                if __debug__: log('sending stop message to UI')
                wx.CallAfter(pub.sendMessage, 'stop')
        elif clicked in [wx.ID_NO, wx.ID_OK]:
            dlg.Destroy()
            frame.Destroy()
            self._queue.put(True)
            if __debug__: log('sending stop message to UI')
            wx.CallAfter(pub.sendMessage, 'stop')
        else:
            dlg.Destroy()
            self._queue.put(True)


    def _current_frame(self):
        '''Returns the current application frame, or a new app frame if none
        is currently active.  This makes it possible to use dialogs when the
        application main window doesn't exist.'''
        if wx.GetApp():
            if __debug__: log('app window exists; building frame for dialog')
            app = wx.GetApp()
            frame = wx.Frame(app.TopWindow)
        else:
            if __debug__: log("app window doesn't exist; creating one for dialog")
            app = wx.App(False)
            frame = wx.Frame(None, -1, __package__)
        frame.Center()
        return frame


    def _wait(self):
        self._queue.get()
