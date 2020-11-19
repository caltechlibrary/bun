#!/usr/bin/env python3

import os
import sys

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from quiche import UI, inform, warn, alert, alert_fatal

# Initialize Quiche ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ui = UI('demo', 'A demonstration of Quiche')
ui.start()

# Demo some Quiche functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

inform('This is an informational message')
warn('This is a warning')
alert('This is an alert')
alert_fatal('This is a fatal alert')

# Say goodbye ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

inform('Done')
