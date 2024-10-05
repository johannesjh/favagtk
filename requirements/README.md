# Favagtk's Flatpak Build

favagtk's flatpak build includes several modules to build and install all the dependencies that are required for favagtk.

- Flatpak build manifest, see `org.gnome.gitlab.johannesjh.favagtk.json`

- Python packages

  - Python dependencies are declared in `requirements/*.in` files.
  - The `requirements/Makefile` provides commands for updating python dependencies. The commands roughly work as follows:
  - `pip-compile` is used to freeze python dependencies.
  - `req2flatpak.py` is used to generate a flatpak build module for the python packages.

## Updating Dependency Versions

To update required dependency versions:

1. Update the version of `org.gnome.Platform` in `requirements/Makefile`, in the flatpak build manifest `org.gnome.gitlab.johannesjh.favagtk.json` and in `.gitlab-ci.yml`
2. Update the target platform version in `requirements/Makefile`
3. Update the list of python packages that come pre-installed as part of `org.gnome.Platform` by running `make -C requirements python3-gnome-platform.in`.
4. Update the list of additional python packages that are needed by favagtk by manually editing `python3-main.in`.
5. Resolve python dependencies by running `make -C requirements pip-compile`.
6. Update the python package versions in the flatpak build module by running `make -C requirements python3-main.json`.

...then build and test favagtk.

## Autoupdating Dependency Versions

The CI configuration in `.gitlab-ci.yml` includes a script to be run periodically.
The script runs pip-compile (by invoking `requirements/Makefile`)
and submits a merge request with updated dependencies.
