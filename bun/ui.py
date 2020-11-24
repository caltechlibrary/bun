'''
cli.py: main interface class for Bun

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by the California Institute of Technology.  This code is
open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

from .base import UIBase
from .cli import CLI


# Exported classes.
# .............................................................................
# This class is essentially a wrapper that deals with selecting the real
# class that should be used for the kind of interface being used.  Internally
# it implements a singleton instance, and provides a method to access that
# instance.

class UI(UIBase):
    '''Wrapper class for the user interface.'''

    __instance = None

    def __new__(cls, name, subtitle = None, show_banner = True,
                use_gui = False, use_color = True, be_quiet = False):
        '''Return an instance of the appropriate user interface handler.'''
        if cls.__instance is None:
            if use_gui:
                from .gui import GUI
                obj = GUI
            else:
                obj = CLI
            cls.__instance = obj(name, subtitle, show_banner,
                                 use_gui, use_color, be_quiet)
        return cls.__instance


    @classmethod
    def instance(cls):
        return cls.__instance


# Exported functions.
# .............................................................................
# These methods get an instance of the UI by themselves and do not require
# callers to do it.  They are meant to be used largely like basic functions
# such as "print()" are used in Python.

def inform(text, *args, **kwargs):
    '''Print an informational message to the user.  The 'text' can contain
    string format placeholders such as "{}", and the additional arguments in
    args are values to use in those placeholders.

    By default, the message will not be printed if the UI has been given
    the "quiet" flag.  However, if this method is passed the keyword
    argument "force" with a value of True, then the "quiet" setting will
    be overridden and the message printed anyway.
    '''
    ui = UI.instance()
    ui.inform(text, *args, **kwargs)


def warn(text, *args):
    '''Warn the user that something is not right.  This should be used in
    situations where the problem is not fatal nor will prevent continued
    execution.  (For problems that prevent continued execution, use the
    alert(...) method instead.)
    '''
    ui = UI.instance()
    ui.warn(text, *args)


def alert(text, *args):
    '''Alert the user to an error.  This should be used in situations where
    there is a problem that will prevent normal execution.
    '''
    ui = UI.instance()
    ui.alert(text, *args)


def alert_fatal(text, *args, **kwargs):
    '''Print or display a message reporting a fatal error.  The keyword
    argument 'details' can be supplied to pass a longer explanation that will
    be displayed (when a GUI is being used) if the user presses the 'Help'
    button in the dialog.

    Note that when a GUI interface is in use, this method will cause the
    GUI to exit after the user clicks the OK button, so that the calling
    application can regain control and exit.
    '''
    ui = UI.instance()
    ui.alert_fatal(text, *args, **kwargs)


def file_selection(type, purpose, pattern = '*'):
    '''Returns the file selected by the user.  The value of 'type' should be
    'open' if the reason for the request is to open a file for reading, and
    'save' if the reason is to save a file.  The argument 'purpose' should be
    a short text string explaining to the user why they're being asked for a
    file.  The 'pattern' is a file pattern expression of the kind accepted by
    wxPython FileDialog.
    '''
    ui = UI.instance()
    return ui.file_selection(type, purpose, pattern)


def login_details(prompt, user, password):
    '''Asks the user for a login name and password.  The value of 'user' and
    'password' will be used as initial values in the dialog.
    '''
    ui = UI.instance()
    return ui.login_details(prompt, user, password)


def confirm(question):
    '''Returns True if the user replies 'yes' to the 'question'.'''
    ui = UI.instance()
    return ui.confirm(question)
