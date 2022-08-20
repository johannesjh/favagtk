# Todos

- Enable dark mode

  - See https://gitlab.gnome.org/johannesjh/favagtk/-/issues/9
  - Make sure the GTK window and widgets respect the system's dark mode,
    see https://developer.gnome.org/documentation/tutorials/beginners/getting_started/dark_mode.html
  - Ask upstream if fava wants to support dark mode styling too,
    the feature only really makes sense if fava's web content is dark as well.

- speed up the build

  - speed up python package installations by rewriting flatpak-pip-generator,
    see https://gitlab.gnome.org/johannesjh/favagtk/-/issues/7
  - update to gnome 43beta,
    which means we don't need a custom webkit anymore
  - move optional packages to a flatpak extension?

- automatic dependency updates
  - see https://gitlab.gnome.org/johannesjh/favagtk/-/issues/8
