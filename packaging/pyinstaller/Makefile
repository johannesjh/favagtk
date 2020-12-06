.PHONY: pyinstaller
pyinstaller: dist/fava-desktop

dist/fava-desktop:
	poetry run pyinstaller pyinstaller.spec

.PHONY: dist/fava-desktop
run: pyinstaller
	./dist/fava-desktop
