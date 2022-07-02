# favagtk flatpak build

favagtk's flatpak build includes several modules to build and install dependencies that are required for favagtk.

- GNOME Target Platform

  - `org.gnome.Platform` is the runtime target platform of favagtk.
  - version numbers for org.gnome.Platform must be identical in `org.gnome.gitlab.johannesjh.favagtk.json` and in `.gitlab-ci.yml`.

- Flatpak build

  - The flathub and flatpak communities have a strong preference for installing third-party dependencies from source instead of using pre-built binaries. These dependencies are built and installed as part of the flatpak build.

  - The `org.gnome.Sdk` platform is used as runtime for favagtk's flatpak build. The Sdk includes compilers and other tools. Whatever is missing in the Sdk must be built and installed from source.

- WebkitGtk

  - A version is needed that is compatible with GTK4.

  - Unfortunately, `org.gnome.Platform//42` does not include a recent enough version of webkitgtk. Possible workarounds include:
    - building and installing a recent build of webkitgtk on top of `org.gnome.Platform//42`, or
    - building development builds against `org.gnome.Platform//master` (which does ship a recent enough version of webkitgtk)
    - wait for a next version of `org.gnome.Platform` to be published.

- Python packages

  - A general note about how python packages are handled in favagtk's flatpak build:

    - `pip-compile` is used to freeze python dependencies.

    - `flatpak-pip-generator` is used to generate flatpak build modules that build and install the according python packages from sources.

    - Some python packages are difficult to build and install from source because they have a lot of compile-time dependencies. In this case, I used hand-written flatpak build modules instead of flatpak-pip-generator.

  - Scikit-learn

    - The `scikit-learn` python package and its transitive dependencies including numpy are difficult to build from source because of its compile-time dependencies. This was solved by using a hand-written flatpak build module for scikit-learn.

## Further References

To generate requirements lists with platform/architecture-specific packages, e.g., with binary wheels:

- [flatpak-pip-generator issue #296 "Allow using binary wheels instead of building from source"](https://github.com/flatpak/flatpak-builder-tools/issues/296)
- [pip-compile-cross-platform](https://pypi.org/project/pip-compile-cross-platform/), similar to pip-compile but using poetry's dependency resolver under the hood.
