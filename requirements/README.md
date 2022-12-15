# Favagtk's Flatpak Build

favagtk's flatpak build includes several modules to build and install all the dependencies that are required for favagtk.

- Flatpak build

  - For the flatpak build manifest, see `org.gnome.gitlab.johannesjh.favagtk.json`
  - Version numbers for org.gnome.Platform must be identical in `org.gnome.gitlab.johannesjh.favagtk.json` and in `.gitlab-ci.yml`.

- Python packages

  - Python dependencies are declared in `requirements/*.in` files.
  - The `requirements/Makefile` provides commands for updating python dependencies. The commands roughly work as follows:
  - `pip-compile` is used to freeze python dependencies.
  - `req2flatpak.py` is used to generate a flatpak build module for the python packages.


## Autoupdates

The CI configuration in `.gitlab-ci.yml` includes a script to be run periodically.
The script runs pip-compile (by invoking `requirements/Makefile`) 
and submits a merge request with updated dependencies.

