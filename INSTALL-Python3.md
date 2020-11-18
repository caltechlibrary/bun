
# Install Python 3.x

Getting your Python setup right on your system is important; otherwise, you may find yourself in the realm of confusing error messages.  The following instructions focus on getting [Python 3](https://docs.python.org/3/) running on Debian/Ubuntu Linux-based systems as well as on macOS via [MacPorts](https://www.macports.org) or [HomeBrew](https://brew.sh).

_**Tip**: If you are running on an Intel-based computers (e.g., most Macs and Windows machines), you can use a Python distribution called [Miniconda](https://docs.conda.io/en/latest/miniconda.html).  This is often the easiest approach to getting a modern Python on your machine.  If that's not suitable for you for any reason, continue on reading._

## Python versions issues

It is possible to use your default OS-provided Python if it is version greater than 3.x. Many distributions still ship with Python version 2.7, and the `pip` command that they provide correspond to Python version 2.7. On some systems, version 3.x of the Python interpreter and `pip` are available using the commands `python3` and `pip3`, respectively. Other systems let you install Python 3 and `pip` via their package manager and use the package manager select default versions and/or names. (This is true on Debian/Ubuntu based systems as well as macOS's MacPorts.)

## Getting the right Python and `pip`

### Debian/Ubuntu

Debian-based systems still ship with older versions of Python by
default. We want to use a modern Python 3.x. Make sure it is 
installed and available along with the related version of pip.

```
sudo apt install python3 python3-pip
```

### macOS

#### _Using MacPorts_

If you are using macOS and MacPorts you can take a similar approach:

```
sudo port install python3
sudo port install py38-pip
```

At this point you should be able to envoke the Python interpreter using the `python3` command. You should see the version of Python and `pip` with these commands:

```
python3 --version
python3 -m pip --version
```

#### _Using HomeBrew_

If you are using macOS and HomeBrew, the corresponding commands are as follows:

```
sudo brew install python3
```

HomeBrew's Python 3 package installs `pip3` by default.  Unless you configured your copy of HomeBrew to install it elsewhere, programs should end up in `/usr/local/bin` on your computer.  Look for a version of `pip` there (e.g., by running the command `ls /usr/local/bin/pip*` to see what gets listed).


### Install Python modules using the right pip

Often you'll need some additional modules to be installed in your Python development environment, so that you can refer to them in your Python programs using the `import` statement. To make sure you get the desired Python and `pip`, you can use the `-m` interpreter option to install the desired module using a command with the following form:

```shell
python3 -m pip install MODULENAME
```

where `MODULENAME` is the name of the module you need to install.
