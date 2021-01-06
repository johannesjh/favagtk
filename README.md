# Fava Desktop

Fava Desktop allows to use the [Fava](https://github.com/beancount/fava) and [Beancount](https://github.com/beancount/beancount) double-entry bookkeeping software packages as a desktop application.

* Makes it easy to install and use fava and beancount. 

* No messing in the commandline, no python virtualenvs  - a convenient way to open and edit beancount files as in any other desktop application.

* Packaged as flatpak application.


## Screenshot

![Screenshot of Fava-Desktop](https://user-images.githubusercontent.com/581188/103780103-d65ef180-5034-11eb-9430-e9ee4dfece87.png)


## Usage

Fava-Desktop has been developed and tested on Linux with GNOME 3.18. Other operating systems may or may not work. 

First clone this repository, then execute the following commands to build, install, and run Fava-Desktop:

```bash
# to build and install a fava-desktop flatpak bundle:
make install

# to run the fava-desktop flatpak bundle:
flatpak run io.github.beancount.FavaDesktop
```

## Development

You can use poetry to develop Fava-Desktop locally. This should work on linux machines with GNOME 3.18. First clone this repository, then execute the following commands.

```bash
# to install pre-commit on your system,
# follow instructions from https://pre-commit.com/, for example:
pip install pre-commit

# to install the pre-commit git hooks in the cloned fava-desktop repo
pre-commit install

# to install required python packages in a virtual environment
poetry install

# to run a commandline shell using the python virtual environment
poetry shell

# to lint the code
pre-commit run

# to run fava-desktop using the python virtual environment
make run
```

## License

Fava-Desktop is MIT licensed, see [LICENSE](./LICENSE) file.

Most of Fava-Desktop's functionality comes from other software packages; many thanks in particular to the authors of of [Fava](https://github.com/beancount/fava) and [Beancount](https://github.com/beancount/beancount). Fava-Desktop's dependencies are licensed differently, see [poetry.lock](./poetry.lock) and [io.github.beancount.FavaDesktop.yml](./packaging/flatpak/io.github.beancount.FavaDesktop.yml) for packages that Fava-Desktop depends on.
