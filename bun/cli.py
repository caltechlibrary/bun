'''
cli.py: command-line interface class for Bun

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by the California Institute of Technology.  This code is
open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

from   commonpy.string_utils import antiformat
import getpass
from   queue import Queue
from   rich import box
from   rich.box import HEAVY, DOUBLE_EDGE, ASCII
from   rich.console import Console
from   rich.panel import Panel
from   rich.style import Style
from   rich.theme import Theme
import shutil
import sys

if __debug__:
    from sidetrack import log

from .base import UIBase


# Constants.
# .............................................................................

_CLI_THEME = Theme({
    'info'        : 'green3',
    'warn'        : 'orange1',
    'warning'     : 'orange1',
    'alert'       : 'red',
    'alert_fatal' : 'bold red',
    'fatal'       : 'bold red',
    'standout'    : 'bold green1',
    'banner'      : 'green3',
})


# Exported classes.
# .............................................................................

class CLI(UIBase):
    '''Command-line interface.'''

    def __init__(self, name, subtitle, show_banner, use_gui, use_color, be_quiet):
        super().__init__(name, subtitle, show_banner, use_gui, use_color, be_quiet)
        if __debug__: log('initializing CLI')
        self._started = False

        # If another thread was eager to send messages before we finished
        # initialization, messages will get queued up on this internal queue.
        self._queue = Queue()

        # Initialize output configuration.
        self._console = Console(theme = _CLI_THEME,
                                color_system = "auto" if use_color else None)

        if show_banner and not be_quiet:
            # We need the plain_text version in any case, to calculate length.
            plain_text = f'Welcome to {name}: {subtitle}'
            fancy_text = f'Welcome to [standout]{name}[/]: {subtitle}'
            text = fancy_text if use_color else plain_text
            terminal_width = shutil.get_terminal_size().columns or 80
            padding = (terminal_width - len(plain_text) - 2) // 2
            # Queueing up this message now will make it the 1st thing printed.
            box_style = DOUBLE_EDGE if use_color else ASCII
            self._print_or_queue(Panel(text, style = 'banner', box = box_style,
                                       padding = (0, padding)), style = 'info')


    def start(self):
        '''Start the user interface.'''
        if __debug__: log('starting CLI')
        while not self._queue.empty():
            (text, style) = self._queue.get()
            self._console.print(text, style = style, highlight = False)
            sys.stdout.flush()
        self._started = True


    def stop(self):
        '''Stop the user interface.'''
        pass


    def _print_or_queue(self, text, style):
        if self._started:
            if __debug__: log(antiformat(text))
            self._console.print(text, style = style, highlight = False)
        else:
            if __debug__: log(f'queueing message "{antiformat(text)}"')
            self._queue.put((text, style))


    def inform(self, text, *args, **kwargs):
        '''Print an informational message.

        By default, the message will not be printed if the UI has been given
        the "quiet" flag.  However, if this method is passed the keyword
        argument "force" with a value of True, then the "quiet" setting will
        be overridden and the message printed anyway.'''
        if ('force' in kwargs and kwargs['force']) or not self._be_quiet:
            self._print_or_queue(text.format(*args), 'info')
        else:
            if __debug__: log(text, *args)


    def warn(self, text, *args):
        '''Print a nonfatal, noncritical warning message.'''
        self._print_or_queue(text.format(*args), style = 'warn')


    def alert(self, text, *args):
        '''Print a message reporting an error.'''
        self._print_or_queue(text.format(*args), style = 'alert')


    def alert_fatal(self, text, *args, **kwargs):
        '''Print a message reporting a fatal error.

        This method returns after execution and does not force an exit of
        the application.  In that sense it mirrors the behavior of the GUI
        version of alert_fatal(...), which also returns, but unlike the GUI
        version, this method does not stop the user interface (because in the
        CLI case, there is nothing equivalent to a GUI to shut down).
        '''
        text += '\n' + kwargs['details'] if 'details' in kwargs else ''
        self._print_or_queue(text.format(*args), style = 'fatal')


    def confirm(self, question):
        '''Asks a yes/no question of the user, on the command line.'''
        return input(f'{question} (y/n) ').startswith(('y', 'Y'))


    def file_selection(self, operation_type, question, pattern):
        '''Ask the user to type in a file path.'''
        return input(operation_type.capitalize() + ' ' + question + ': ')


    def login_details(self, prompt, user = None, pswd = None):
        '''Returns a tuple of user, password, and a Boolean indicating
        whether the user cancelled the dialog.  If 'user' is provided, then
        this method offers that as a default for the user.  If both 'user'
        and 'pswd' are provided, both the user and password are offered as
        defaults but the password is not shown to the user.  If the user
        responds with empty strings, the values returned are '' and not None.
        '''
        try:
            text = (prompt + ' [default: ' + user + ']: ') if user else (prompt + ': ')
            input_user = input(text)
            if len(input_user) == 0:
                input_user = user
            hidden = ' [default: ' + '*'*len(pswd) + ']' if pswd else ''
            text = 'Password' + (' for "' + user + '"' if user else '') + hidden + ': '
            input_pswd = _password(text)
            if len(input_pswd) == 0:
                input_pswd = pswd
            final_user = '' if input_user is None else input_user
            final_pswd = '' if input_pswd is None else input_pswd
            return final_user, final_pswd, False
        except KeyboardInterrupt:
            return user, pswd, True


# Miscellaneous utilities
# .............................................................................

def _password(prompt):
    # If it's a tty, use the version that doesn't echo the password.
    if sys.stdin.isatty():
        return getpass.getpass(prompt)
    else:
        sys.stdout.write(prompt)
        sys.stdout.flush()
        return sys.stdin.readline().rstrip()
