# Contributing

All contributions to favagtk are greatly appreciated... pull requests are welcome, and so are bug reports and suggestions for improvement.

## Viewing Debug Output

Starting favagtk from the commandline allows to view its debug output and helps understand what is going on "under the hood". This can be useful to analyze a problem prior to reporting a bug.

```bash
flatpak run org.gnome.gitlab.johannesjh.favagtk
```

## Setting up a Development Environment

Simply clone this project in GNOME Builder.

## Build Options

See [docs/build-options.md](./docs/build-options.md)
for how to configure build options.

## Dependencies

favagtk depends on other software packages.
These dependencies are defined in the following files.

- Flatpak's packaging definition in `org.gnome.gitlab.johannesjh.favagtk.json`,
  as well as in other files referenced there
- The `meson.build` files
- Python dependencies in the `requirements` folder.

favagtk aims for compatibility with the package versions defined there.

## Code quality

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

## Flatpak Packaging

favagtk is packaged using flatpak.

- You can build a package locally GNOME Builder by simply clicking the build button.
- Gitlab's ci integration also creates package builds.

## Releases

Releases are named using semantic versioning.
They are built in gitlab ci; the build is triggered by pushing a tag:

- To prepare a release, don't forget to update the appdata file, to describe the release and its changes.
- Optionally, create a release candidate by pushing a tag named similar to `v1.2.3-rc4`.
- To create the release, push a tag named similar to `v1.2.3`.

All releases are available for download on [favagtk's release page](https://gitlab.gnome.org/johannesjh/favagtk/-/releases)
