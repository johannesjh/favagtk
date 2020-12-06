.PHONY: pyinstaller
pyinstaller: dist/fava-desktop

dist/fava-desktop:
	poetry run pyinstaller pyinstaller.spec

.PHONY: run
run: pyinstaller
	./dist/fava-desktop

.PHONY: clean
clean:
	rm -rf build dist
