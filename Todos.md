# Development Todos

- Implement keyboard shortcuts
  - Ctrl-O for opening a file
  - Ctrl-Q for closing the application
- Integrate with github CI (`pre-commit run --all`, build and run using poetry, build and run using flatpak)
- Clean up dependency management:
  - Current mess: We are currently declaring some dependencies in pyproject.toml and some in the Makefile.
  - Future considerations: Should we keep vendoring the fava dependency using git? It would be simpler if fava could release their current master branch as a new version, then I could simply depend on it using pip/poetry. Alternatively, Fava-Desktop could depend on Fava using a pip reference to fava's git repository - but this would likely require to overwrite fava's setup.py's build command in order to trigger the frontend build when fava is installed from git sources. See end of this article [How To Add Custom Build Steps and Commands To setup.py](https://jichu4n.com/posts/how-to-add-custom-build-steps-and-commands-to-setuppy/)
- Cleanup versioning, publish releases (should be possible using github ci?)
