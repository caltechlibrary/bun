import os
import pytest
import sys

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from quiche import UI, inform, warn, alert, alert_fatal


def test_quiet(capsys):
    ui = UI('test', 'description of test', be_quiet = True)
    ui.start()
    inform('foo')
    out, err = capsys.readouterr()
    assert out == ''
    warn('foo')
    out, err = capsys.readouterr()
    assert out == 'foo\n'
    alert('foo')
    out, err = capsys.readouterr()
    assert out == 'foo\n'
