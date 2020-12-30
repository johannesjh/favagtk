.PHONY: all
all: clean flatpak

.PHONY: install
install: clean
	make -C packaging/flatpak install

.PHONY: clean
clean:
	@echo "\n\nCleaning up..."
	-poetry run pyclean fava_desktop tests
	rm -rf .pytest_cache __pycache__ build dist fava
	make -C packaging/flatpak clean

fava:
	@echo "\n\nCloning and building fava..."
	git clone --single-branch --branch master --depth 1 https://github.com/beancount/fava.git
	make -C fava

.PHONY: run
run: fava
	@echo "\n\nRunning fava_desktop from local sources..."
	poetry install
	poetry run python3 fava_desktop/main.py


.PHONY: test
test:
	@echo "\n\nRunning pytest..."
	poetry run pytest

dist: fava
	@echo "\n\nCreating python wheels..."
	poetry run pip3 wheel --wheel-dir dist ./fava
	poetry run pip3 wheel --wheel-dir dist smart-importer
	poetry build

.PHONY: flatpak
flatpak: dist
	@echo "\n\nInvoking the flatpak package build..."
	make -C packaging/flatpak dist
	@echo "\nDone building the flatpak bundle."
	@ls packaging/flatpak/dist/*.flatpak
