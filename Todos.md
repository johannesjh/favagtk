# Development Todos

- Cleanup versioning, publish releases (should be possible using github ci?)
- Integrate with github CI (`pre-commit run --all`, build and run using poetry, build and run using flatpak)
- Parse commandline arguments (and pass them on to fava), e.g., see `do_commandline` in https://python-gtk-3-tutorial.readthedocs.io/en/latest/application.html#application
- Display File Name in header bar (possible by binding the header bar to an observable property?)
- Consider building flatpak packages using GNOME Builder and meson since this appears to be the default way of doing things?
- Consider building a mac package.
