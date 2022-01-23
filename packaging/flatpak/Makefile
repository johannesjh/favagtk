.PHONY: default
default: clean dist

.PHONY: clean
clean:
	rm -rf build dist

.PHONY: build
build: build/app

build/app:
	mkdir -p build/app
	touch build/.trackerignore
	flatpak-builder --state-dir=build/state --repo=build/repo build/app io.github.beancount.FavaGtk.yml #--build-shell=fava-gtk

.PHONY: install
install: build/app
	flatpak-builder --user --install --force-clean --state-dir=build/state --repo=build/repo build/app io.github.beancount.FavaGtk.yml

.PHONY: dist
dist: dist/io.github.beancount.FavaGtk.flatpak

dist/io.github.beancount.FavaGtk.flatpak: build/app
	desktop-file-validate io.github.beancount.FavaGtk.desktop
	appstreamcli validate io.github.beancount.FavaGtk.appdata.xml
	mkdir -p dist
	touch dist/.trackerignore
	flatpak build-bundle build/repo dist/io.github.beancount.FavaGtk.flatpak io.github.beancount.FavaGtk

.PHONY: dist-install
dist-install: uninstall dist/io.github.beancount.FavaGtk.flatpak
	flatpak --user install -y dist/io.github.beancount.FavaGtk.flatpak

.PHONY: uninstall
uninstall:
	-flatpak --user uninstall -y io.github.beancount.FavaGtk

.PHONY: run
run:
	flatpak run io.github.beancount.FavaGtk
