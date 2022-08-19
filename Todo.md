# Todos

- fix the ci build
  - the gnome gitlab ci script has changed,
    I need to adapt favagtk's ci script to that, 
    see https://gitlab.gnome.org/GNOME/Initiatives/-/wikis/DevOps-with-Flatpak

- fix occasional crash because of threading problem
  https://gitlab.gnome.org/johannesjh/favagtk/-/issues/6 

- update fava to 1.22.3
- update fava-investor to 0.3.0
  https://github.com/redstreet/fava_investor/releases
- update other packages

- refactor the build
  - update to gnome 43beta, 
    which means we don't need a custom webkit anymore
  - move optional packages to a flatpak extension?
  - speed up the build by installing pandas from binary package,
    e.g., as part of the scikit-learn flatpak build json

- Enable dark mode

  - Make sure the GTK window and widgets respect the system's dark mode,
    see https://developer.gnome.org/documentation/tutorials/beginners/getting_started/dark_mode.html
  - Ask upstream if fava wants to support dark mode styling too,
    the feature only really makes sense if fava's web content is dark as well.

- Consider using flatpak extensions for additional packages
  e.g., for smart_importer, which is large because it needs scikit-learn.
