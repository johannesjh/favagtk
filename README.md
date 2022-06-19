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

All contributions are greatly appreciated... pull requests are welcome, and so are bug reports and suggestions for improvement. See [CONTRIBUTING.md](./CONTRIBUTING.md) for details, e.g., how to view debug output when testing and how to setup a development environment.

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
