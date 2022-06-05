# Conditions evaluation

## start program
```sh
python3 main.py
```
Quit it by pressing `Ctrl+d`

## how to write a condition?
Everyting in () is a boolean, like `(1 < 2)` or `(False)`
since this is recursive, `((((False))))` is a valid boolean, as `False` is too.

Booleans can be chained using || (OR) and && (AND) like `(1<2) && (False)` with a limit of 2 conditions.

For a AND chain on 3 conditions, we can write it like so `True and (True and True)`.
