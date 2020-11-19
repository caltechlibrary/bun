'''
app_frame.py: wxPython GUI definition for the GUI frame

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2018-2020 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

from   commonpy.module_utils import datadir_path
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
import textwrap
from   threading import Thread
import webbrowser

if __debug__:
    from sidetrack import set_debug, log, logr

from .logo import getLogoIcon


# Exported classes.
# .............................................................................

class AppFrame(wx.Frame):
    '''Defines the main application GUI frame.'''

    def __init__(self, name, subtitle, *args, **kwds):
        if sys.platform.startswith('win'):
            self._scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)/100
        else:
            self._scale_factor = 1

        self._name = name
        self._subtitle = subtitle
        self._cancel = False
        self._height = 316 if self._scale_factor > 1.5 else 320
        self._height *= self._scale_factor
        self._width  = 500
        self._width  *= self._scale_factor

        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL
        wx.Frame.__init__(self, *args, **kwds)
        self.panel = wx.Panel(self)
        headline = self._name + ((' — ' + self._subtitle) if self._subtitle else '')
        self.headline = wx.StaticText(self.panel, wx.ID_ANY, headline, style = wx.ALIGN_CENTER)
        self.headline.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC,
                                      wx.FONTWEIGHT_BOLD, 0, "Arial"))

        # For macos, I figured out how to make the background color of the text
        # box be the same as the rest of the UI elements.  That looks nicer for
        # our purposes (IMHO) than the default (which would be white), but then
        # we need a divider to separate the headline from the text area.
        if not sys.platform.startswith('win'):
            self.divider1 = wx.StaticLine(self.panel, wx.ID_ANY)
            self.divider1.SetMinSize((self._width, 2))

        text_area_size = (self._width, 200 * self._scale_factor)
        self.text_area = wx.richtext.RichTextCtrl(self.panel, wx.ID_ANY,
                                                  size = text_area_size,
                                                  style = wx.TE_MULTILINE | wx.TE_READONLY)

        # Quit button on the bottom.
        self.divider2 = wx.StaticLine(self.panel, wx.ID_ANY)
        self.quit_button = wx.Button(self.panel, label = "Quit")
        self.quit_button.Bind(wx.EVT_KEY_DOWN, self.on_cancel_or_quit)

        # On macos, the color of the text background is set to the same as the
        # rest of the UI panel.  I haven't figured out how to do it on Windows.
        if not sys.platform.startswith('win'):
            gray = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND)
            self.text_area.SetBackgroundColour(gray)

        # Create a simple menu bar.
        self.menuBar = wx.MenuBar(0)

        # Add a "File" menu with a quit item.
        self.fileMenu = wx.Menu()
        self.exitItem = wx.MenuItem(self.fileMenu, wx.ID_EXIT, "&Exit",
                                    wx.EmptyString, wx.ITEM_NORMAL)
        self.fileMenu.Append(self.exitItem)
        if sys.platform.startswith('win'):
            # Only need to add a File menu on Windows.  On Macs, wxPython
            # automatically puts the wx.ID_EXIT item under the app menu.
            self.menuBar.Append(self.fileMenu, "&File")

        # Add a "help" menu bar item.
        self.helpMenu = wx.Menu()
        self.helpItem = wx.MenuItem(self.helpMenu, wx.ID_HELP, "&Help",
                                    wx.EmptyString, wx.ITEM_NORMAL)
        self.helpMenu.Append(self.helpItem)
        self.helpMenu.AppendSeparator()
        self.aboutItem = wx.MenuItem(self.helpMenu, wx.ID_ABOUT,
                                     "&About " + self._name,
                                     wx.EmptyString, wx.ITEM_NORMAL)
        self.helpMenu.Append(self.aboutItem)
        self.menuBar.Append(self.helpMenu, "Help")

        # Put everything together and bind some keystrokes to events.
        self.SetMenuBar(self.menuBar)
        self.Bind(wx.EVT_MENU, self.on_cancel_or_quit, id = self.exitItem.GetId())
        self.Bind(wx.EVT_MENU, self.on_help, id = self.helpItem.GetId())
        self.Bind(wx.EVT_MENU, self.on_about, id = self.aboutItem.GetId())
        self.Bind(wx.EVT_CLOSE, self.on_cancel_or_quit)
        self.Bind(wx.EVT_BUTTON, self.on_cancel_or_quit, self.quit_button)

        close_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.on_cancel_or_quit, id = close_id)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('W'), close_id )])
        self.SetAcceleratorTable(accel_tbl)

        # Now that we created all the elements, set layout and placement.
        self.SetSize((self._width, self._height))
        self.SetTitle(self._name)
        self.outermost_sizer = wx.BoxSizer(wx.VERTICAL)
        self.outermost_sizer.AddSpacer(5)
        self.outermost_sizer.Add(self.headline, 0, wx.ALIGN_CENTER, 0)
        if not sys.platform.startswith('win'):
            self.outermost_sizer.AddSpacer(5)
            self.outermost_sizer.Add(self.divider1, 0, wx.EXPAND, 0)
            self.outermost_sizer.AddSpacer(5)
        self.outermost_sizer.Add(self.text_area, 0, wx.EXPAND, 0)
        self.outermost_sizer.AddSpacer(5)
        if not sys.platform.startswith('win'):
            self.outermost_sizer.Add(self.divider2, 0, wx.EXPAND, 0)
            self.outermost_sizer.AddSpacer(5)
        self.outermost_sizer.AddSpacer(5 * self._scale_factor)
        self.outermost_sizer.Add(self.quit_button, 0, wx.BOTTOM | wx.CENTER, 0)
        if not sys.platform.startswith('win'):
            self.outermost_sizer.AddSpacer(5)
        self.SetSizer(self.outermost_sizer)
        self.Layout()
        self.Centre()

        # Finally, hook in message-passing interface.
        pub.subscribe(self.login_dialog, "login_dialog")
        pub.subscribe(self.info_message, "info_message")
        pub.subscribe(self.open_file, "open_file")
        pub.subscribe(self.save_file, "save_file")


    def on_cancel_or_quit(self, event):
        if __debug__: log('got Exit/Cancel')
        self._cancel = True
        wx.BeginBusyCursor()
        self.info_message('\nStopping work – this may take a few moments ...\n')

        # We can't call pub.sendMessage from this function, nor does it work
        # to call it using wx.CallAfter directly from this function: both
        # methods hang the GUI and the progress message is never printed.
        # Calling it from a separate thread works.

        def quitter():
            if __debug__: log('sending message to quit')
            wx.CallAfter(pub.sendMessage, 'stop')

        subthread = Thread(target = quitter)
        subthread.start()
        return True


    def on_escape(self, event):
        if __debug__: log('got Escape')
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.on_cancel_or_quit(event)
        else:
            event.Skip()
        return True


    def on_about(self, event):
        if __debug__: log('opening About window')
        dlg = wx.adv.AboutDialogInfo()
        dlg.SetName(self._name)
        this_module = sys.modules[__package__]
        dlg.SetVersion(this_module.__version__)
        dlg.SetLicense(this_module.__license__)
        dlg.SetDescription('\n'.join(textwrap.wrap(this_module.__description__, 81)))
        dlg.SetWebSite(this_module.__url__)
        dlg.AddDeveloper(this_module.__author__)
        dlg.SetIcon(getLogoIcon())
        wx.adv.AboutBox(dlg)
        return True


    def on_help(self, event):
        if __debug__: log('opening Help window')
        wx.BeginBusyCursor()
        help_file = path.join(datadir_path(__package__), "help.html")
        if readable(help_file):
            webbrowser.open_new("file://" + help_file)
        wx.EndBusyCursor()
        return True


    def info_message(self, message):
        self.text_area.SetInsertionPointEnd()
        self.text_area.AppendText(message + '\n')
        self.text_area.ShowPosition(self.text_area.GetLastPosition())
        return True


    def open_file(self, return_queue, message, pattern = '*.*'):
        if __debug__: log('creating and showing open file dialog')
        fd = wx.FileDialog(self, 'Open ' + message, defaultDir = os.getcwd(),
                           wildcard = pattern,
                           style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        cancelled = (fd.ShowModal() == wx.ID_CANCEL)
        file_path = None if cancelled else fd.GetPath()
        if cancelled:
            if __debug__: log('user cancelled dialog')
        else:
            if __debug__: log('file path from user: {}', file_path)
        return_queue.put(file_path)


    def save_file(self, return_queue, message):
        if __debug__: log('creating and showing save file dialog')
        fd = wx.FileDialog(self, 'Save ' + message, defaultDir = os.getcwd(),
                           style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        cancelled = (fd.ShowModal() == wx.ID_CANCEL)
        file_path = None if cancelled else fd.GetPath()
        if cancelled:
            if __debug__: log('user cancelled dialog')
        else:
            if __debug__: log('file path from user: {}', file_path)
        return_queue.put(file_path)


    def login_dialog(self, results, user, password):
        if __debug__: log('creating and showing login dialog')
        dialog = LoginDialog(self, self._name)
        dialog.initialize_values(results, user, password)
        dialog.ShowWindowModal()


class LoginDialog(wx.Dialog):
    '''Defines the modal dialog used for getting the user's login credentials.'''

    def __init__(self, parent, app_name):
        super(LoginDialog, self).__init__(parent)

        if sys.platform.startswith('win'):
            self._scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)/100
        else:
            self._scale_factor = 1

        self._name = app_name
        self._user = None
        self._password = None
        self._cancel = False
        self._wait_queue = None

        panel = wx.Panel(self)
        if sys.platform.startswith('win'):
            self.SetSize((360 * self._scale_factor, 160 * self._scale_factor))
        else:
            self.SetSize((330, 155))
        self.explanation = wx.StaticText(panel, wx.ID_ANY,
                                         self._name + ' needs your login credentials',
                                         style = wx.ALIGN_CENTER)
        if sys.platform.startswith('win'):
            self.explanation.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC,
                                             wx.FONTWEIGHT_NORMAL, 0, "Arial"))
        self.top_line = wx.StaticLine(panel, wx.ID_ANY)
        self.login_label = wx.StaticText(panel, wx.ID_ANY, "Caltech login: ", style = wx.ALIGN_RIGHT)
        self.login = wx.TextCtrl(panel, wx.ID_ANY, '', style = wx.TE_PROCESS_ENTER)
        self.login.Bind(wx.EVT_KEY_DOWN, self.on_enter_or_tab)
        self.login.Bind(wx.EVT_TEXT, self.on_text)
        self.password_label = wx.StaticText(panel, wx.ID_ANY, "Caltech password: ", style = wx.ALIGN_RIGHT)
        self.password = wx.TextCtrl(panel, wx.ID_ANY, '', style = wx.TE_PASSWORD)
        self.password.Bind(wx.EVT_KEY_DOWN, self.on_enter_or_tab)
        self.password.Bind(wx.EVT_TEXT, self.on_text)
        self.bottom_line = wx.StaticLine(panel, wx.ID_ANY)
        self.cancel_button = wx.Button(panel, wx.ID_ANY, "Cancel")
        self.cancel_button.Bind(wx.EVT_KEY_DOWN, self.on_escape)
        self.ok_button = wx.Button(panel, wx.ID_ANY, "OK")
        self.ok_button.Bind(wx.EVT_KEY_DOWN, self.on_ok_enter_key)
        self.ok_button.SetDefault()
        self.ok_button.Disable()

        # Put everything together and bind some keystrokes to events.
        self.__set_properties()
        self.__do_layout()
        self.Bind(wx.EVT_BUTTON, self.on_cancel_or_quit, self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.on_ok, self.ok_button)
        self.Bind(wx.EVT_CLOSE, self.on_cancel_or_quit)

        close_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.on_cancel_or_quit, id = close_id)
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('W'), close_id ),
            (wx.ACCEL_CMD, ord('.'), close_id ),
        ])
        self.SetAcceleratorTable(accel_tbl)


    def __set_properties(self):
        self.SetTitle(self._name)
        self.login_label.SetToolTip("The account name.")
        self.login.SetMinSize((195 * self._scale_factor, 22 * self._scale_factor))
        self.password_label.SetToolTip("The account password.")
        self.password.SetMinSize((195 * self._scale_factor, 22 * self._scale_factor))
        self.ok_button.SetFocus()


    def __do_layout(self):
        self.outermost_sizer = wx.BoxSizer(wx.VERTICAL)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.login_sizer = wx.FlexGridSizer(2, 2, 5, 0)
        self.outermost_sizer.Add((360 * self._scale_factor, 5 * self._scale_factor), 0, wx.ALIGN_CENTER, 0)
        self.outermost_sizer.Add(self.explanation, 0, wx.ALIGN_CENTER, 0)
        self.outermost_sizer.Add((360 * self._scale_factor, 5 * self._scale_factor), 0, wx.ALIGN_CENTER, 0)
        self.outermost_sizer.Add(self.top_line, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        self.outermost_sizer.Add((360 * self._scale_factor, 8 * self._scale_factor), 0, wx.ALIGN_CENTER, 0)
        self.login_sizer.Add(self.login_label, 0, wx.ALIGN_RIGHT, 0)
        self.login_sizer.Add(self.login, 0, wx.EXPAND, 0)
        self.login_sizer.Add(self.password_label, 0, wx.ALIGN_RIGHT, 0)
        self.login_sizer.Add(self.password, 0, wx.EXPAND, 0)
        self.outermost_sizer.Add(self.login_sizer, 1, wx.ALIGN_CENTER | wx.FIXED_MINSIZE, 5)
        if sys.platform.startswith('win'):
            self.outermost_sizer.Add((360, 10 * self._scale_factor), 0, 0, 0)
        else:
            self.outermost_sizer.Add((360, 5), 0, 0, 0)
        self.outermost_sizer.Add(self.bottom_line, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        self.outermost_sizer.Add((360 * self._scale_factor, 5), 0, 0, 0)
        self.button_sizer.Add((0, 0), 0, 0, 0)
        self.button_sizer.Add(self.cancel_button, 0, wx.ALIGN_CENTER, 0)
        self.button_sizer.Add((10, 20), 0, 0, 0)
        self.button_sizer.Add(self.ok_button, 0, wx.ALIGN_CENTER, 0)
        self.button_sizer.Add((10, 20), 0, wx.ALIGN_CENTER, 0)
        self.outermost_sizer.Add(self.button_sizer, 1, wx.ALIGN_RIGHT, 0)
        self.outermost_sizer.Add((360 * self._scale_factor, 5), 0, wx.ALIGN_CENTER, 0)
        self.SetSizer(self.outermost_sizer)
        self.Layout()
        self.Centre()


    def initialize_values(self, wait_queue, user, password):
        '''Initializes values used to populate the dialog and communicate
        with calling code.

        'wait_queue' must be a Pytho queue.Queue() object.  Callers must
        create the queue object and pass it to this function.  After creating
        and displaying the dialog, callers can use .get() on the queue object
        to wait until the user has either clicked OK or Cancel in the dialog.

        'user' and 'password' are used to populate the credentials form in
        case there are preexisting values to be used as defaults.'''

        self._wait_queue = wait_queue
        self._user = user
        self._password = password
        if self._user:
            self.login.AppendText(self._user)
            self.login.Refresh()
        if self._password:
            self.password.AppendText(self._password)
            self.password.Refresh()


    def return_values(self):
        if __debug__: log('return_values called')
        self._wait_queue.put((self._user, self._password, self._cancel))


    def inputs_nonempty(self):
        user = self.login.GetValue()
        password = self.password.GetValue()
        if user.strip() and password.strip():
            return True
        return False


    def on_ok(self, event):
        '''Stores the current values and destroys the dialog.'''

        if __debug__: log('got OK')
        if self.inputs_nonempty():
            self._cancel = False
            self._user = self.login.GetValue()
            self._password = self.password.GetValue()
            self.return_values()
            # self.Destroy()
            self.return_values()
            self.EndModal(event.EventObject.Id)
        else:
            if __debug__: log('has incomplete inputs')
            self.complain_incomplete_values(event)


    def on_cancel_or_quit(self, event):
        if __debug__: log('got Cancel')
        self._cancel = True
        self.return_values()
        # self.Destroy()
        self.return_values()
        self.EndModal(event.EventObject.Id)


    def on_text(self, event):
        if self.login.GetValue() and self.password.GetValue():
            self.ok_button.Enable()
        else:
            self.ok_button.Disable()


    def on_escape(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            if __debug__: log('got Escape')
            self.on_cancel_or_quit(event)
        else:
            event.Skip()


    def on_ok_enter_key(self, event):
        keycode = event.GetKeyCode()
        if keycode in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER, wx.WXK_SPACE]:
            self.on_ok(event)
        elif keycode == wx.WXK_ESCAPE:
            self.on_cancel_or_quit(event)
        else:
            event.EventObject.Navigate()


    def on_enter_or_tab(self, event):
        keycode = event.GetKeyCode()
        if keycode in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
            # If the ok button is enabled, we interpret return/enter as "done".
            if self.ok_button.IsEnabled():
                self.on_ok(event)
            # If focus is on the login line, move to password.
            if wx.Window.FindFocus() is self.login:
                event.EventObject.Navigate()
        elif keycode == wx.WXK_TAB:
            event.EventObject.Navigate()
        elif keycode == wx.WXK_ESCAPE:
            self.on_cancel_or_quit(event)
        else:
            event.Skip()


    def complain_incomplete_values(self, event):
        dialog = wx.MessageDialog(self, caption = "Missing login and/or password",
                                  message = "Incomplete values – do you want to quit?",
                                  style = wx.YES_NO | wx.ICON_WARNING,
                                  pos = wx.DefaultPosition)
        response = dialog.ShowModal()
        dialog.EndModal(wx.OK)
        dialog.Destroy()
        if (response == wx.ID_YES):
            self._cancel = True
            self.return_values()
