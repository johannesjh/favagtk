.PHONY: build
build: build/fava-desktop

.PHONY: clean
clean:
	rm -rf .flatpak-builder .pytest_cache build dist flatpak-builder-tools generated-poetry-sources.json


# FLATPAK BUILD

build/fava-desktop:
	make -C ../.. dist
	flatpak-builder --force-clean --state-dir=build/.flatpak-builder --repo=build/fava-desktop-repo build/fava-desktop io.github.beancount.fava-desktop.yml  #--build-shell=fava-desktop


# FLATPAK INSTALL AND RUN

.PHONY: install
install: build
	@-flatpak --user uninstall -y io.github.beancount.fava-desktop
	@-flatpak --user remote-delete fava-desktop-repo
	flatpak --user remote-add --no-gpg-verify fava-desktop-repo build/fava-desktop-repo
	flatpak --user install -y fava-desktop-repo io.github.beancount.fava-desktop

.PHONY: run
run: install
	flatpak run io.github.beancount.fava-desktop


# FLATPAK BUNDLE

.PHONY: bundle
bundle: dist/fava-desktop.flatpak

dist/fava-desktop.flatpak: build/fava-desktop
	mkdir -p dist
	flatpak build-bundle build/fava-desktop-repo dist/fava-desktop.flatpak io.github.beancount.fava-desktop


.PHONY: run-bundle
run-bundle: dist/fava-desktop.flatpak
	@-flatpak --user uninstall -y io.github.beancount.fava-desktop
	flatpak --user install -y dist/fava-desktop.flatpak
	flatpak run io.github.beancount.fava-desktop
