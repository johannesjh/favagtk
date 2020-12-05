.PHONY: run
run:
	poetry run python3 fava_desktop/main.py

.PHONY: clean
clean:
	poetry run pyclean .

.PHONY: test
test:
	poetry run pytest

.PHONY: pyinstaller
pyinstaller: dist/fava-desktop

dist/fava-desktop:
	poetry run pyinstaller pyinstaller.spec
