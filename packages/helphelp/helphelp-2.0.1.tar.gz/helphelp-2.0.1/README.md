# Command-line help on Python modules, classes and functions

This package procures the command-line tool **`pyh`**. It works somewhat like UNIX's
[`man`](https://fr.wikipedia.org/wiki/Man_%28Unix%29), but for Python's docstring-based help system. In a nutshell:

```
$ pyh print
print(...)
    print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)

    Prints the values to a stream, or to sys.stdout by default.
    Optional keyword arguments:
    file:  a file-like object (stream); defaults to the current sys.stdout.
    sep:   string inserted between values, default a space.
    end:   string appended after the last value, default a newline.
    flush: whether to forcibly flush the stream.
```

A more complex example:

```
$ pyh pathlib Path.is_file
Help on function is_file in module pathlib:

is_file(self)
    Whether this path is a regular file (also True for symlinks pointing
    to regular files).
```

To shorten the command lines a bit, one can configure a set of their favorite aliases for modules names in file
`$XDG_CONFIG_HOME/pyh/aliases` (which typically resolves to `$HOME/.config/pyh/aliases`). The alias file is written in
the [NestedText](https://nestedtext.org/en/stable/) format, which looks similar to YAML. One simply encodes an
alias-to-module name dictionary, one line per entry. Example:

```
pd: pandas
pl: pathlib
ap: argparse
```

---

## Installing

`pip install pyh`

## Development

Setting up the development environment relies on [Conda](https://docs.conda.io/en/latest/). Clone the repository, `cd`
into the local copy, then

```
$ conda env create
```

Dependent packages are managed through the `environment.yml` file. When changing dependencies, update the development
environment with command

```
$ conda env update
```
