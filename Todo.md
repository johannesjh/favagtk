# Todos

- speed up build by installing pandas from binary package
  as part of the scikit-learn flatpak build json

- Do I need to sandbox webkit?, as proposed in this initiative:
  https://gitlab.gnome.org/GNOME/Initiatives/-/wikis/Sandbox-all-the-WebKit!

  - Note: Do a regression test to see if documents can still be added
    by dragging them unto a fava journal entry.

- Enable dark mode

  - Make sure the GTK window and widgets respect the system's dark mode,
    see https://developer.gnome.org/documentation/tutorials/beginners/getting_started/dark_mode.html
  - Ask upstream if fava wants to support dark mode styling too,
    the feature only really makes sense if fava's web content is dark as well.

- Consider using flatpak extensions for additional packages
  e.g., for smart_importer, which is large because it needs scikit-learn.
