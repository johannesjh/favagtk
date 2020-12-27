# Fava Desktop 

Fava Desktop provides the Fava and Beancount double-entry bookkeeping software as desktop application. 

Technically, Fava Desktop wraps Fava's web user interface in a GNOME GTK application. The web interface is rendered in a WebKit webview. The application is packaged using flatpak.


## Todos

* Change the flatpak application id to use underscore instead of dash (because app data files don't accept application IDs with dashes)
* Provide an app data file /app/share/metainfo/io.github.beancount.fava_desktop.appdata.xml, e.g., using the online generator https://www.freedesktop.org/software/appstream/metainfocreator/#/guiapp
* Choose a license (MIT similar to fava?)
* Integrate with github CI (`pre-commit run --all`, build and run using poetry, build and run using flatpak)
