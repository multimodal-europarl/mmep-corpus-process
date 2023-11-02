# docs

A dir for documentation.

## update

From project root:
```
pdoc -t docs/dark-mode/ -o docs/docs scripts/
```

## howto

Everything you want documented needs to have a doc string. Folders need an `__init__.py` file. You can source markdown into the docstring with:
```
.. include:: README.md
```