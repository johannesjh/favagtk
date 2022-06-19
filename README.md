# favagtk

[![pipeline status](https://gitlab.gnome.org/johannesjh/favagtk/badges/main/pipeline.svg)](https://gitlab.gnome.org/johannesjh/favagtk/-/commits/main)
[![Latest Release](https://gitlab.gnome.org/johannesjh/favagtk/-/badges/release.svg)](https://gitlab.gnome.org/johannesjh/favagtk/-/releases)

Do your finances using fava and beancount.

favagtk makes it easy to use the
[Fava](https://github.com/beancount/fava) and
[Beancount](https://github.com/beancount/beancount)
double-entry bookkeeping software as a GNOME desktop application.

- Easy installation using flatpak.

- Start fava and beancount as you would any other desktop application.

- Built as a GNOME application, using GTK and webkit, packaged using flatpak.

## Screenshot

![Screenshot of favagtk](https://gitlab.gnome.org/johannesjh/favagtk/raw/HEAD/data/screenshots/main.png)

## Getting Started

In the future, favagtk will be published on [flathub](https://flathub.org/). As for now, the easiest way to start using Fava GTK is to download and install a flatpak application package from [favagtk's releases in gilab](https://gitlab.gnome.org/johannesjh/favagtk/-/releases).

### System Requirements

A linux system with [flatpak](https://flatpak.org/) is needed to install and run the flatpak package.

### Installation

Download a .flatpak file from one of [favagtk's releases in gitlab](https://gitlab.gnome.org/johannesjh/favagtk/-/releases).

You can then install the application as follows.

```bash
flatpak install --user <file.flatpak>
```

### Usage

Once installed, you will find an application named "Fava" that can be started in the very same way as any other desktop application, e.g., using GNOME Shell.

The application window that is initially shown prompts to open a beancount file. If you don't have a beancount file yet, you can simply create an empty text file with a `.beancount` extension. Alternatively, it is possible to generate an example beancount file by running [beancount's bean-example command](https://beancount.github.io/docs/tutorial_example.html#generate-an-example-file). Opening the beancount file will display fava's user interface, allowing to view and edit the beancount file.

Note that FavaGTK is only a thin convenience layer around [Fava](https://github.com/beancount/fava) and [Beancount](https://github.com/beancount/beancount). These two programs provide the actual functionality. You can find documentation on how to use these programs for managing your finances on their respective websites.

## Contributing

All contributions are greatly appreciated... pull requests are welcome, and so are bug reports and suggestions for improvement.

### Viewing Debug Output

Starting favagtk from the commandline allows to view its debug output and helps understand what is going on "under the hood". This can be useful to analyze a problem prior to reporting a bug.

```bash
flatpak run org.gnome.gitlab.johannesjh.favagtk
```

### Setting up a Development Environment

Simply clone this project in GNOME Builder.

### Build Options

See [docs/build-options.md](./docs/build-options.md)
for how to configure build options.

### Dependencies

favagtk depends on other software packages.
These dependencies are defined in the following files.

- Flatpak's packaging definition in `org.gnome.gitlab.johannesjh.favagtk.json`,
  as well as in other files referenced there
- The `meson.build` files
- Python dependencies in the `requirements` folder.

favagtk aims for compatibility with the package versions defined there.

### Code quality

Use [pre-commit](https://pre-commit.com/) to prettify and lint the code before committing changes.

```bash
# to install pre-commit on your system,
# follow instructions from https://pre-commit.com/, for example:
pip install pre-commit  # install pre-commit using pip

# to install the pre-commit git hooks in the cloned favagtk repo
pre-commit install  # activates pre-commit in the current git repo

# to prettify and lint all code
pre-commit run --all

# to prettify and lint only staged changes
pre-commit run
```

### Flatpak Packaging

favagtk is packaged using flatpak-builder.
You can build the project in GNOME Builder by simply clicking the build button.

### Releases

Releases are named using semantic versioning.
They are built in gitlab ci; the build is triggered by pushing a tag:

- To prepare a release, don't forget to update the appdata file, to describe the release and its changes.
- Optionally, create a release candidate by pushing a tag named similar to `v1.2.3-rc4`.
- To create the release, push a tag named similar to `v1.2.3`.

All releases are available for download on [favagtk's release page](https://gitlab.gnome.org/johannesjh/favagtk/-/releases)

## License

favagtk is GPL-licensed, see the [LICENSE](./LICENSE) file.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

Licenses of packages that favagtk depends on:
Most of favagtk's functionality comes from other software packages;
many thanks in particular to the authors of
[Fava](https://github.com/beancount/fava)
and [Beancount](https://github.com/beancount/beancount).
See the `requirements` folder for a list of software packages
that favagtk depends on.
