'''
ui_base.py: base classes for Bun

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by the California Institute of Technology.  This code is
open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''


# Base class for UI implementations
# .............................................................................
# This class is not meant to be accessed by external code directly.  The
# classes below subclass from this one and provide the actual implementations
# for the methods depending on the type of interface (GUI or CLI).

class UIBase:
    '''Base class for user interface classes.'''

    def __init__(self, name, subtitle, show_banner, use_gui, use_color, be_quiet):
        ''''name' is the name of the application.  'subtitle' is a short
        string shown next to the name, in the form "name -- subtitle".
        'use_gui' indicates whether a GUI or CLI interface should be used.
        'use_color' applies only to the CLI, and indicates whether terminal
        output should be colored to indicate different kinds of messages.
        Finally, 'be_quiet' also applies only to the CLI and, if True,
        indicates that informational messages should not be printed.
        '''
        self._name        = name
        self._subtitle    = subtitle
        self._show_banner = show_banner
        self._use_gui     = use_gui
        self._use_color   = use_color
        self._be_quiet    = be_quiet


    def is_gui(self):
        return self._use_gui


    def app_name(self):
        return self._name


    def app_subtitle(self):
        return self._subtitle


    # Methods for starting and stopping the interface -------------------------

    def start(self): raise NotImplementedError
    def stop(self):  raise NotImplementedError


    # Methods to show messages to the user ------------------------------------

    def inform(self, text, *args, **kwargs):          raise NotImplementedError
    def warn(self, text, *args):                      raise NotImplementedError
    def alert(self, text, *args):                     raise NotImplementedError
    def alert_fatal(self, text, *args, **kwargs):     raise NotImplementedError


    # Methods to ask the user -------------------------------------------------

    def file_selection(self, type, purpose, pattern): raise NotImplementedError
    def login_details(self, prompt, user, pswd):      raise NotImplementedError
    def confirm(self, question):                      raise NotImplementedError
