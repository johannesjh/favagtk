# Fava GTK

Fava GTK allows to use the [Fava](https://github.com/beancount/fava) and [Beancount](https://github.com/beancount/beancount) double-entry bookkeeping software packages as a desktop application.

* Makes it easy to install and use fava and beancount.

* No messing in the commandline, no python virtualenvs  - a convenient way to open and edit beancount files as in any other desktop application.

* Built using GTK, packaged as flatpak application.


## Screenshot

![Screenshot of fava-gtk](https://user-images.githubusercontent.com/581188/104773200-fa2ce080-5774-11eb-978a-654c62511104.png)


## Usage

fava-gtk has been developed and tested on Linux with GNOME 3.18. Other operating systems may or may not work.

First clone this repository, then execute the following commands to build, install, and run fava-gtk:

```bash
# to build and install a fava-gtk flatpak bundle:
make -C packaging/flatpak install

# to run the fava-gtk flatpak bundle:
flatpak run io.github.beancount.FavaGtk
```

## Development

To run fava-gtk from local sources, clone this repository, then execute the following commands.

```bash
# to install required python packages in a virtual environment
poetry install

# to run fava-gtk using the python virtual environment
make run
```

Lint before committing changes:

```bash
# to install pre-commit on your system,
# follow instructions from https://pre-commit.com/, for example:
pip install pre-commit

# to install the pre-commit git hooks in the cloned fava-gtk repo
pre-commit install

# to lint all code
pre-commit run --all

# to lint staged changes
pre-commit run
```


## License

fava-gtk is MIT licensed, see [LICENSE](./LICENSE) file.

Most of fava-gtk's functionality comes from other software packages; many thanks in particular to the authors of of [Fava](https://github.com/beancount/fava) and [Beancount](https://github.com/beancount/beancount). fava-gtk's dependencies are licensed differently, see [poetry.lock](./poetry.lock) and [io.github.beancount.FavaGtk.yml](./packaging/flatpak/io.github.beancount.FavaGtk.yml) for packages that fava-gtk depends on.
