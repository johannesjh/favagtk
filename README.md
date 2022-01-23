# Fava GTK

![main branch build status](https://github.com/johannesjh/fava-gtk/workflows/CI/badge.svg?branch=main)

Fava GTK allows to use the [Fava](https://github.com/beancount/fava) and [Beancount](https://github.com/beancount/beancount) double-entry bookkeeping software packages as a desktop application.

* Makes it easy to install and use fava and beancount.

* Simple installation using flatpak, no messing in the commandline  - a convenient way to open and edit beancount files as in any other desktop application.

* Built using GTK and webkit, packaged as flatpak application.

## Screenshot

![Screenshot of fava-gtk](https://user-images.githubusercontent.com/581188/111044548-8b54c680-8449-11eb-94cb-c74b2294a670.png)

## Getting Started

The easiest way to start using Fava GTK is to download and install the flatpak application package from the Fava GTK releases on Github, as detailed in the following.

### System Requirements

Fava GTK has been developed and tested on Linux with GNOME 3.38. Other operating systems and desktop environments may or may not work. [flatpak](https://flatpak.org/) is needed to install and run the flatpak package.

### Installation

Download a .flatpak file from one of Fava GTK's releases on github.

You can then install the application as follows.

```bash
flatpak install --user <file.flatpak>
```

### Usage

Once installed, you will find an application named "Fava" that can be started in the very same way as any other desktop application, e.g., using GNOME Shell.

The application window that is initially shown prompts to open a beancount file. If you don't have a beancount file yet, you can simply create an empty text file with a `.beancount` extension. Opening the beancount file will display fava's user interface, allowing to view and edit the beancount file.

Fava GTK is only a thin convenience layer around [Fava](https://github.com/beancount/fava) and [Beancount](https://github.com/beancount/beancount). These two programs provide the actual functionality. You will find documentation on how to use these programs for managing your finances on their respective websites.

## Contributing

All contributions are greatly appreciated... pull requests welcome, and so are bug reports and suggestions for improvement.

### Viewing Debug Output

Starting Fava GTK from the commandline allows to view its debug output and helps understand what is going on "under the hood". This can be useful to analyze a problem prior to reporting a bug.

```bash
flatpak run io.github.beancount.FavaGtk
```

### Setting up a Development Environment

Fava GTK is written as a python application using the GTK user interface toolkit and targeting the GNOME desktop environment. The following requirements are needed to develop and run Fava GTK straight from its python source code.

System requirements: A modern GNOME installation will usually come with everything you need.

* [python3](https://www.python.org/) is needed, no support for python2. See setup.cfg for the specific version of python that is required.
* [PyGObject](https://pygobject.readthedocs.io/) is needed because it provides language bindings to GTK. If you are running GNOME you most certainly have it on your system already. Have a look at [PyGObject's installation instructions](https://pygobject.readthedocs.io/en/latest/getting_started.html) and choose (or try out to see) if you want to install PyGObject using pip or using your operating system's package manager.
* [WebKitGTK](https://webkitgtk.org/) must be installed, specifically WebKit2 API Level4. If you are running GNOME, you probably have it on your system already.
* Optionally [Glade](https://glade.gnome.org) in order to edit .ui files.

Setting up the development environment: The [Makefile](./Makefile) provides commands that make it easy to set up a python virtual environment for developing Fava GTK.

```bash
# Run this command to create a python virtual environment for Fava GTK.
# PyGObject is used from your system-wide installation.
# All other dependencies are installed using locked version numbers in the virtualenv.
# Fava GTK is installed in the virtualenv in editable mode.
make venv

# To start Fava GTK using your virtual environment:
make run
```

### Python Dependencies

Fava GTK depends on other python packages, as defined in the `requirements/*.in` files. Fava GTK aims for compatibility with the version ranges defined in these files. 

Version-locked aka "frozen" requirement definitions are automatically generated using [pip-compile-multi](https://pypi.org/project/pip-compile-multi/). The resulting files are named `requirements/*.txt`. These files specify a specific package version for all direct and indirect dependencies. This allows to create reproduceable development environments and package builds.

Modifying python dependencies works as follows:

* Minor Upgrades within the constraints of `requirements/*.in`: Simply run `pip-compile-multi`. This will lock packages to their newest version, within the given constraints. Don't forget to test if the application still works correctly. 
* Major Upgrades: Check if some of the packages in `requirements/*.in` exist in a newer version. Manually edit the `requirements/*.in` files, then proceed as with minor updates. I.e., run `pip-compile-multi` to update the frozen package versions and don't forget to test if the application still works correctly.
* Adding additional python dependencies: Specify the additional requirements in one of the `requirements/*.in` files, then run `pip-compile-multi`.

### Code quality

Use [pre-commit](https://pre-commit.com/) to lint the code before committing changes.

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

### Flatpak Packaging

Fava GTK is packaged using flatpak-builder. The following software is needed to build flatpak application packages.

* flatpak-builder (installed using instructions from https://docs.flatpak.org/en/latest/first-build.html)
* appstream (provides the appstreamcli command, which is used to validate the appstream xml file)
* desktop-file-utils (provides the desktop-file-validate command, which is used to validate the desktop file)

Have a look at the targets available in [the flatpak packaging Makefile](./packaging/flatpak/Makefile). These targets build, install and launch the Fava GTK .flatpak application package. For example:

```bash
# to create a flatpak bundle
cd packaging/flatpak
make
```

### Release Process

How to release a new version of Fava GKT

* Test the flatpak image. Given that functional changes are already tested using the dev setup, a quick smoke test should suffice to verify that the flatpak build is working.
* Edit the version number in `setup.cfg` to match the version that shall be released, git commit and push. Format the version number as, e.g., `1.2.3`.
* Tag the same version number, prefixed with letter `v`, e.g., `v1.2.3`, then run `git push --tags`
* Github's ci should build the flatpak package and upload it to a release with the same name.
* Edit the release notes on the github releases page, and paste the same release notes into the CHANGES file.
* Optionally set a next development version number in setup.cfg, e.g., `1.2.4-dev`, push changes.

## License

fava-gtk is GPL-licensed, see the [LICENSE](./LICENSE) file.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Licenses of packages that fava-gtk depends on: Most of fava-gtk's functionality comes from other software packages; many thanks in particular to the authors of of [Fava](https://github.com/beancount/fava) and [Beancount](https://github.com/beancount/beancount). fava-gtk's dependencies are each licensed in their own way, see the requirements definitions in this repo for lists of packages that fava-gtk depends on.
