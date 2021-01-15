FLATPAK_ID = io.github.beancount.FavaGtk

# FEATURED TARGETS

.PHONY: build
build: clean build/app

.PHONY: dist
dist: clean dist/${FLATPAK_ID}.flatpak

.PHONY: run
run: clean dist/run

.PHONY: install
install: clean dist/install

.PHONY: clean
clean:
	rm -rf build dist


# BUILD AND RUN THE APP USING A LOCAL FLATPAK REPOSITORY

.PHONY: build/app
build/app: build/lint
	make -C ../.. dist
	@echo "\n\nBuilding the flatpak app..."
	flatpak-builder --force-clean --state-dir=build/state --repo=build/repo build/app ${FLATPAK_ID}.yml  #--build-shell=fava-gtk

.PHONY: build/lint
build/lint:
	desktop-file-validate ${FLATPAK_ID}.desktop
	appstreamcli validate ${FLATPAK_ID}.appdata.xml

.PHONY: build/uninstall
build/uninstall:
	@echo "\n\nUninstallig the flatpak app and the local build repo..."
	-flatpak --user uninstall -y ${FLATPAK_ID}
	-flatpak --user remote-delete ${FLATPAK_ID}_REPO

.PHONY: build/install
build/install: build/app build/uninstall
	@echo "\n\nInstalling the flatpak app from the local build repo..."
	flatpak --user remote-add --no-gpg-verify ${FLATPAK_ID}_REPO build/repo
	flatpak --user install -y ${FLATPAK_ID}_REPO ${FLATPAK_ID}

.PHONY: build/run
build/run: build/install
	@echo "\n\nRunning the flatpak app..."
	flatpak run ${FLATPAK_ID}


# CREATE AND RUN A FLATPAK BUNDLE

dist/${FLATPAK_ID}.flatpak: build/app
	@echo "\n\nCreating a .flatpak bundle..."
	mkdir -p dist
	flatpak build-bundle build/repo dist/${FLATPAK_ID}.flatpak ${FLATPAK_ID}

.PHONY: dist/uninstall
dist/uninstall:
	@echo "\n\nUninstalling the flatpakk app..."
	-flatpak --user uninstall -y ${FLATPAK_ID}

.PHONY: dist/install
dist/install: dist/uninstall dist/${FLATPAK_ID}.flatpak
	@echo "\n\nInstalling the .flatpak bundle..."
	flatpak --user install dist/${FLATPAK_ID}.flatpak

.PHONY: dist/run
dist/run: dist/install
	@echo "\n\nRunning the flatpak app..."
	flatpak run ${FLATPAK_ID}
