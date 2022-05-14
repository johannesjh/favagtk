# Fava GTK

[![pipeline status](https://gitlab.gnome.org/johannesjh/favagtk/badges/main/pipeline.svg)](https://gitlab.gnome.org/johannesjh/favagtk/-/commits/main)

Fava GTK allows to use the [Fava](https://github.com/beancount/fava) and [Beancount](https://github.com/beancount/beancount) double-entry bookkeeping software packages as a desktop application.

- Easy installation using flatpak.

- Start fava and beancount as you would any other desktop application.

- Built using GTK and webkit, packaged as flatpak application.

## Screenshot

![Screenshot of fava-gtk](https://gitlab.gnome.org/johannesjh/favagtk/raw/HEAD/data/screenshots/main.png)

## Getting Started

In the future, favagtk will be published on [flathub](https://flathub.org/). As for now, the easiest way to start using Fava GTK is to download and install a flatpak application package from the [CI pipelines](https://gitlab.gnome.org/johannesjh/favagtk/-/pipelines).

### System Requirements

A linux system with [flatpak](https://flatpak.org/) is needed to install and run the flatpak package.

### Installation

Download a .flatpak file from one of Fava GTK's [CI builds over on GNOME Gitlab](https://gitlab.gnome.org/johannesjh/favagtk).

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

Simply clone this project in GNOME Builder.

### Python Dependencies

Fava GTK depends on other python packages, as defined in the requirements folder.
Fava GTK aims for compatibility with the package versions defined there.

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

Fava GTK is packaged using flatpak-builder.
You can build the project in GNOME Builder by simply clicking the build button.

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
  see the requirements folder for lists of packages that fava-gtk depends on.
