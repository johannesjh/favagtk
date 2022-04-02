# Fava GTK

![main branch build status](https://github.com/johannesjh/fava-gtk/workflows/CI/badge.svg?branch=main)

Fava GTK allows to use the [Fava](https://github.com/beancount/fava) and [Beancount](https://github.com/beancount/beancount) double-entry bookkeeping software packages as a desktop application.

- Easy installation using flatpak.

- Start fava and beancount as you would any other desktop application.

- Built using GTK and webkit, packaged as flatpak application.

## Screenshot

![Screenshot of fava-gtk](https://user-images.githubusercontent.com/581188/111044548-8b54c680-8449-11eb-94cb-c74b2294a670.png)

## Getting Started

The easiest way to start using Fava GTK is to download and install a flatpak application package from the [releases on Github](https://github.com/johannesjh/fava-gtk/releases), as detailed in the following.

### System Requirements

Fava GTK has been developed and tested on Linux with GNOME 41.
Other operating systems and desktop environments may or may not work.
[flatpak](https://flatpak.org/) is needed to install and run the flatpak package.

### Installation

Download a .flatpak file from one of Fava GTK's releases on github.

You can then install the application as follows.

```bash
flatpak install --user <file.flatpak>
```

### Usage

Once installed, you will find an application named "Fava" that can be started in the very same way as any other desktop application, e.g., using GNOME Shell.

The application window that is initially shown prompts to open a beancount file. If you don't have a beancount file yet, you can simply create an empty text file with a `.beancount` extension. Opening the beancount file will display fava's user interface, allowing to view and edit the beancount file.

FavaGTK is only a thin convenience layer around [Fava](https://github.com/beancount/fava) and [Beancount](https://github.com/beancount/beancount). These two programs provide the actual functionality. You can find documentation on how to use these programs for managing your finances on their respective websites.

## Contributing

All contributions are greatly appreciated... pull requests are welcome, and so are bug reports and suggestions for improvement.

### Viewing Debug Output

Starting Fava GTK from the commandline allows to view its debug output and helps understand what is going on "under the hood". This can be useful to analyze a problem prior to reporting a bug.

```bash
flatpak run io.github.beancount.FavaGtk
```

### Setting up a Development Environment

Simply open this project in GNOME Builder.

### Python Dependencies

Fava GTK depends on other python packages, as defined in flatpak-pip-update-modules.sh.
Fava GTK aims for compatibility with the packages defined there.

### Code quality

Use [pre-commit](https://pre-commit.com/) to prettify and lint the code before committing changes.

```bash
# to install pre-commit on your system,
# follow instructions from https://pre-commit.com/, for example:
pip install pre-commit  # install pre-commit using pip

# to install the pre-commit git hooks in the cloned fava-gtk repo
pre-commit install  # activates pre-commit in the current git repo

# to prettify and lint all code
pre-commit run --all

# to prettify and lint only staged changes
pre-commit run
```

### Flatpak Packaging

Fava GTK is packaged using flatpak-builder. The easiest way to build is using GNOME Builder.

## License

fava-gtk is GPL-licensed, see the [LICENSE](./LICENSE) file.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

Licenses of packages that fava-gtk depends on:
Most of fava-gtk's functionality comes from other software packages;
many thanks in particular to the authors of of [Fava](https://github.com/beancount/fava)
and [Beancount](https://github.com/beancount/beancount).

- FavaGtk's dependencies are each licensed in their own way,
  see the .json files for lists of packages that fava-gtk depends on.
- The recents file menu is heavily inspired by
  [apostrophe's open_popover](https://gitlab.gnome.org/World/apostrophe/-/blob/aa56131abdb2839edfec4d6ce3fbbdea9b1bfdd4/apostrophe/open_popover.py)
