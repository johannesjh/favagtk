# Todos

- Test manually

- Publish on flathub
  - Using a separate repository on github, similar to how everybody else
    seems to be keeping dev vs packaging repos separate.
  - Using org.gnome.Platform//42 instead of //master,
    hence including our own build of webkit-gtk, similar to
    [gfeeds](https://github.com/flathub/org.gabmus.gfeeds)
- Do I need to sandbox webkit?, as proposed in this initiative:
  https://gitlab.gnome.org/GNOME/Initiatives/-/wikis/Sandbox-all-the-WebKit!

  - Note: Do a regression test to see if documents can still be added
    by dragging them unto a fava journal entry.

- Enable dark mode

  - Ask upstream if fava wants to support dark mode styling too,
    the feature only really makes sense if fava's web content is dark as well.

- Consider using flatpak extensions for additional packages
  e.g., for smart_importer, which is large because it needs scikit-learn.
