# Contributing

All contributions to favagtk are greatly appreciated... pull requests are welcome, and so are bug reports and suggestions for improvement.

## Testing and Reporting Issues

The easiest way to start contributing is by simply using favagtk and by reporting any errors or inconveniences you may encounter as [issues in favagtk's gitlab project](https://gitlab.gnome.org/johannesjh/favagtk/-/issues). You can test official versions as well as development builds.

For example, it would be most welcome if you'd be willing to test [autoupdate merge requests](https://gitlab.gnome.org/johannesjh/favagtk/-/merge_requests?state=opened&search=autoupdate) by installing and running the .flatpak files from these merge requests. This way, you can help keeping favagtk up to date.

## Installing a Development Build

You can download, install and run a favagtk .flatpak file to benefit from a new feature, as well as for testing.

Downloads are available for each of
[favagtk's releases](https://gitlab.gnome.org/johannesjh/favagtk/-/releases)
and from merge requests and other ci pipelines.

Once downloaded, you can install and run the flatpak file as follows.

```bash
flatpak install --user <file>.flatpak
```

Once installed, you will have an app named "Fava" on your computer.

## Starting the App and Viewing Debug Output

Once installed, the app be started in the same way as any other application, e.g., [using GNOME Shell's activity view](https://help.gnome.org/users/gnome-help/stable/shell-apps-open.html.hi). You can alternatively start favagtk from the commandline, as follows, in order to view its debug output. The debug output logs what is going on "under the hood" and includes error messages and exceptions. This information is useful to analyze a problem prior to reporting a bug.

To start favagtk from the commandline and view its debug output:

```bash
flatpak run org.gnome.gitlab.johannesjh.favagtk
```

## Setting up a Development Environment

Simply clone this project in GNOME Builder and hit the build and run buttons.

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

On a general note:
Releases are named using semantic versioning.
They are built and published using CI scripts when a tag is pushed.

### Releases in the Git Development Repo

To publish a new version of favagtk in favagtk's development repository,
take the following steps:

- Create a branch for the release, e.g., a branch called `v1.2.3`.
- Set the intended version number in the main `meson.build` file.
- Describe the release in the `data/*appdata.xml*` file.
- Commit and push these changes.
- Build a release candidate by pushing a tag named similar to `v1.2.3-rc4`.
- Test the release candidate by downloading and installing the `*.flatpak` file from the build pipeline.
- If tests were ok, merge the release branch into main.
- Publish the release by pushing a tag such as `v1.2.3`.
- Prepare the next release by setting a dev version number such as `v1.2.4-dev` in meson.build on the main branch.

CI scripts will build a package and make it available for download on [favagtk's release page](https://gitlab.gnome.org/johannesjh/favagtk/-/releases) in gitlab.

## Flathub Releases

To publish an updated flatpak package on flathub,
create a pull request with updated manifest and requirement files
in [favagtk's flathub packaging repo](https://github.com/flathub/org.gnome.gitlab.johannesjh.favagtk).

- Flathub's build bot will then start building the app based on the pull request.
- Wait for the build to succeed
- Manually smoketest the build result.
- Merge the pull request
- Flathub build bot will then publish the app.
