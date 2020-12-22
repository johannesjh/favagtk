.PHONY: build
build: build/fava-desktop

.PHONY: clean
clean:
	rm -rf .flatpak-builder .pytest_cache build dist flatpak-builder-tools generated-poetry-sources.json


# FLATPAK BUILD

build/fava-desktop: build/generated-poetry-sources.json
	make -C ../.. build
	flatpak-builder --force-clean --state-dir=build/.flatpak-builder --repo=build/fava-desktop-repo build/fava-desktop io.github.beancount.fava-desktop.yml

build/generated-poetry-sources.json: build/flatpak-builder-tools
	poetry run python3 ./build/flatpak-builder-tools/poetry/flatpak-poetry-generator.py -o build/generated-poetry-sources.json "../../poetry.lock"

build/flatpak-builder-tools:
	git clone --depth 1 https://github.com/flatpak/flatpak-builder-tools.git build/flatpak-builder-tools


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
