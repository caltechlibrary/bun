# Change log for Bun

## Version 0.0.6

This release tweaks the default colors a little bit and adds a new function, `validated_input(...)`. It also fixes a banner text centering bug.


## Version 0.0.5

This version removes the as-yet unfinished GUI code (and associated dependencies from `requirements.txt`). The code is now in a separate branch (`gui`) pending further development in the future.


## Version 0.0.4

Use `antiformat` in certain places to guard against incoming strings that may have single `{` and/or `}` characters. The latter causes errors when they're passed to Python's string `format`.


## Version 0.0.3

Renamed this project **Bun** to avoid a PyPI project name collision with the former name, Quiche.


## Version 0.0.2

Add basic GUI code originally developed for other programs.  It is almost functional.


## Version 0.0.1

First release.
