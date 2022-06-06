# Conditions evaluation

## start program
```sh
python3 main.py
```
Quit it by pressing `Ctrl+d`

## how to write a condition?
everyting in () is a boolean, like `(1 < 2)` or `(False)`
since this is recursive, `((((False))))` is a valid boolean, as `False` is too.

Booleans can be chained using || (OR) and && (AND) like `(1<2) && (False)`

Conditions can be inverted by using the `!` operator.