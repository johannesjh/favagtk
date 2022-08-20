# Contributing

All contributions to favagtk are greatly appreciated... pull requests are welcome, and so are bug reports and suggestions for improvement.

## Viewing Debug Output

Starting favagtk from the commandline allows to view its debug output and helps understand what is going on "under the hood". This can be useful to analyze a problem prior to reporting a bug.

```bash
flatpak run org.gnome.gitlab.johannesjh.favagtk
```

## Setting up a Development Environment

Simply clone this project in GNOME Builder.

The project includes two build configurations:

- `org.gnome.gitlab.johannesjh.favagtk.devel.json`
  for quicker development builds, and
- `org.gnome.gitlab.johannesjh.favagtk.json`
  for release builds.

To choose a build configuration in GNOME Builder,
switch to the "Build Preferences" surface (e.g., using the dropdown button in the top left corner of the window),
select the desired build configuration
and click the "Make Active" button.

## Build Options

Available options are declared in `meson_options.txt`.

### Debug versus Release Builds

The "profile" option allows to toggle between a debug and release build.

The option (as well as other options) can be set in the following ways:

- In GNOME Builder's build options,
  by entering `-Dprofile=release` under "configure options".
  This modifies the flatpak `.json` manifest file.

- In the flatpak manifest `.json` file, the build can be configured
  as follows:

  ```json
  {
    "name": "favagtk",
    "config-opts": ["-Dprofile=release"]
  }
  ```

- If building from the commandline, the build option can be set as follows:
  `meson configure -Dprofile=release`.
  See the [meson documentation about build options](https://mesonbuild.com/Build-options.html)
  for further explanation.

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

On a generaral note:
Releases are named using semantic versioning.
They are built and published using CI scripts when a tag is pushed.

### Releases in the Git Development Repo

To publish a new version of favagtk in favagtk's development repository,
take the following steps:

- Set the intended version number in the main `meson.build` file.
- Describe the release in the `data/*appdata.xml*` file.
- Build and test a release candidate by pushing a tag named similar to `v1.2.3-rc4`.
- Publish the release by pushing a tag named similar to `v1.2.3`.

CI scripts will build a package and make it available for download on [favagtk's release page](https://gitlab.gnome.org/johannesjh/favagtk/-/releases) in gitlab.

## Flathub Releases

To publish an updated flatpak package on flathub,
create a pull request with updated manifest and requirement files
in [favagtk's flathub packaging repo](https://github.com/flathub/org.gnome.gitlab.johannesjh.favagtk).
