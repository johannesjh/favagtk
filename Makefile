.PHONY: all
all: clean flatpak

.PHONY: install
install: clean
	make -C packaging/flatpak install

.PHONY: clean
clean:
	@echo "\n\nCleaning up..."
	-poetry run pyclean fava_gtk tests
	rm -rf .pytest_cache __pycache__ build dist
	make -C packaging/flatpak clean

.PHONY: run
run:
	@echo "\n\nRunning fava_gtk from local sources..."
	poetry install
	poetry run python3 fava_gtk/main.py


.PHONY: test
test:
	@echo "\n\nRunning pytest..."
	poetry run pytest ./tests

dist:
	@echo "\n\nCreating python wheels..."
	poetry build --format wheel
	poetry run pip3 wheel --wheel-dir dist dist/fava_gtk*.whl

.PHONY: flatpak
flatpak: dist
	@echo "\n\nInvoking the flatpak package build..."
	make -C packaging/flatpak dist
	@echo "\nDone building the flatpak bundle."
	@ls packaging/flatpak/dist/*.flatpak
