# Fava GTK

Fava GTK allows to use the [Fava](https://github.com/beancount/fava) and [Beancount](https://github.com/beancount/beancount) double-entry bookkeeping software packages as a desktop application.

* Makes it easy to install and use fava and beancount.

* Simple installation using flatpak, no messing in the commandline  - a convenient way to open and edit beancount files as in any other desktop application.

* Built using GTK and webkit, packaged as flatpak application.


## Screenshot

![Screenshot of fava-gtk](https://user-images.githubusercontent.com/581188/104773200-fa2ce080-5774-11eb-978a-654c62511104.png)


## Getting Started

The easiest way to start using Fava GTK is to download and install the flatpak application package from the Fava GTK releases on Github, as detailed in the following.


### System Requirements

Fava GTK has been developed and tested on Linux with GNOME 3.38. Other operating systems and desktop environments may or may not work. [flatpak](https://flatpak.org/) is needed to install and run the flatpak package.


### Installation

Downloading a .flatpak file from one of Fava GTK's releases on github.

You can then install the application as follows.

```bash
flatpak install --user <file.flatpak>
```


### Usage

Once installed, you will find an application named "Fava" that can be started in the very same way as any other desktop application, e.g., using GNOME Shell.

Alternatively, it is also possible to start Fava GTK from the commandline as follows. This can be useful if you want to see debug output.

```bash
flatpak run io.github.beancount.FavaGtk
```

The application window that is initially shown prompts to open a beancount file. Opening a beancount file will display fava's user interface, allowing to view and edit the beancount file.

Fava GTK is only a think convenience layer around [Fava](https://github.com/beancount/fava) and [Beancount](https://github.com/beancount/beancount). These two programs provide the actual functionality. You will find documentation on how to use these programs for managing your finances on their respective websites.


## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are greatly appreciated. Pull requests welcome.


### Development Environment

Fava GTK is written as a python application using the GTK user interface toolkit and targeting the GNOME desktop environment. The following requirements are needed to develop and run Fava GTK straight from its python source code.

System requirements:

* [python3](https://www.python.org/) is needed, no support for python2. See setup.cfg for the specific version of python that is required.
* [PyGObject](https://pygobject.readthedocs.io/) is needed because it provides language bindings to GTK. If you are running GNOME you most certainly have it on your system already. Have a look at [PyGObject's installation instructions](https://pygobject.readthedocs.io/en/latest/getting_started.html) and choose (or try out to see) if you want to install PyGObject using pip or using your operating system's package manager.
* [WebKitGTK](https://webkitgtk.org/) must be installed, specifically WebKit2 API Level4. If you are running GNOME, you probably have it on your system already.
* git and make


Python package dependencies:

* Fava GTK depends on other python packages, as defined in the `requirements/*.in` files. Fava GTK aims for compatibility with the dependency versions defined in these files.

* Version-locked aka "frozen" requirement definitions can be found in the `requirements/*.txt` files. These files are created automatically using [pip-compile-multi](https://pypi.org/project/pip-compile-multi/). The version-locked requirements allow to create reproduceable development environments and package builds.

The [Makefile](./Makefile) provides useful commands for setting up and using a Fava GTK python virtual environment for development purposes.

```bash
# Run this command to create a python virtual environment for Fava GTK.
# PyGObject is used from your system-wide installation.
# All other dependencies are installed using locked version numbers in the virtualenv.
# Fava GTK is installed in the virtualenv in editable mode.
make venv

# To start Fava GTK using your virtual environment:
make run
```


### Code quality

Use pre-commit to lint the code before committing changes:

```bash
# to install pre-commit on your system,
# follow instructions from https://pre-commit.com/, for example:
pip install pre-commit  # install pre-commit using pip

# to install the pre-commit git hooks in the cloned fava-gtk repo
pre-commit install  # activates pre-commit in the current git repo

# to lint all code
pre-commit run --all

# to lint staged changes
pre-commit run
```


### Flatpak packaging

Fava GTK is packaged using flatpak-builder.

The following additional system requirements are needed to locally build flatpak application packages.

* flatpak-builder (installed using instructions from https://docs.flatpak.org/en/latest/first-build.html, the GNOME SDK will also be installed as part of the build process)
* appstream (provides the appstreamcli command)
* desktop-file-utils (provides the desktop-file-validate command)

Have a look at the targets available in [packaging/flatpak/Makefile]. These targets build, install and launch the .flatpak application package. For example:

```bash
# to create a flatpak bundle
make dist
```


## License

fava-gtk is MIT licensed, see [LICENSE](./LICENSE) file.

Most of fava-gtk's functionality comes from other software packages; many thanks in particular to the authors of of [Fava](https://github.com/beancount/fava) and [Beancount](https://github.com/beancount/beancount). fava-gtk's dependencies are licensed differently, see the requirements definitions in this repo for lists of packages that fava-gtk depends on.
