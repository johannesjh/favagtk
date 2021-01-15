# Development Todos

- Clean up dependency management:
  - Current mess: We are currently declaring some dependencies in pyproject.toml and some in the Makefile.
  - Considerations: Should we keep vendoring the fava dependency using git? It would be simpler if fava could release their current master branch as a new version, then I could simply depend on it using pip/poetry. Alternatively, Fava-Desktop could depend on Fava using a pip reference to fava's git repository - but this would likely require to overwrite fava's setup.py's build command in order to trigger the frontend build when fava is installed from git sources. See end of this article [How To Add Custom Build Steps and Commands To setup.py](https://jichu4n.com/posts/how-to-add-custom-build-steps-and-commands-to-setuppy/)
  - Solution: fava_desktop should depend on fava using git, see https://github.com/beancount/fava/pull/1213  
- Cleanup versioning, publish releases (should be possible using github ci?)
- Integrate with github CI (`pre-commit run --all`, build and run using poetry, build and run using flatpak)
- Parse commandline arguments (and pass them on to fava), e.g., see `do_commandline` in https://python-gtk-3-tutorial.readthedocs.io/en/latest/application.html#application
- Display File Name in header bar (possible by binding the header bar to an observable property?)
- Consider building flatpak packages using GNOME Builder and meson since this appears to be the default way of doing things?
- Consider building a mac package.
