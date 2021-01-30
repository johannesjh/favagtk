.PHONY: default
default: clean dist

.PHONY: clean
clean:
	rm -rf build dist

.PHONY: dist
dist: dist/io.github.beancount.FavaGtk.flatpak

dist/io.github.beancount.FavaGtk.flatpak:
	desktop-file-validate io.github.beancount.FavaGtk.desktop
	appstreamcli validate io.github.beancount.FavaGtk.appdata.xml
	mkdir -p build dist && rm -rf build/app
	touch build/.trackerignore dist/.trackerignore
	flatpak-builder --state-dir=build/state --repo=build/repo build/app io.github.beancount.FavaGtk.yml  #--build-shell=fava-gtk
	flatpak build-bundle build/repo dist/io.github.beancount.FavaGtk.flatpak io.github.beancount.FavaGtk

.PHONY: install
install: uninstall dist/io.github.beancount.FavaGtk.flatpak
	flatpak --user install -y dist/io.github.beancount.FavaGtk.flatpak

.PHONY: uninstall
uninstall:
	-flatpak --user uninstall -y io.github.beancount.FavaGtk
