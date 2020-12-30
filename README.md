# Fava Desktop

Fava Desktop allows to install and use the [Fava](https://github.com/beancount/fava) and [Beancount](https://github.com/beancount/beancount) double-entry bookkeeping software packages as a desktop application.

Fava Desktop makes it easy to install and use fava and beancount. Users can start the application and view and edit beancount files as in any other desktop application - no more need to worry about python environments or commandline instructions.

### Todos

* Make it possible to pip-install fava with a git reference. This will likely require to overwrite setup.py's build command in order to trigger the frontend build. See end of this article https://jichu4n.com/posts/how-to-add-custom-build-steps-and-commands-to-setuppy/
* Implement keyboard shortcuts
  * Ctrl-O for opening a file
  * Ctrl-Q for closing the application
* Integrate with github CI (`pre-commit run --all`, build and run using poetry, build and run using flatpak)
