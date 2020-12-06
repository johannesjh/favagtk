.PHONY: build
build:
	poetry build

.PHONY: run
run:
	poetry run python3 fava_desktop/main.py

.PHONY: clean
clean:
	rm -rf .pytest_cache build dist
	poetry run pyclean fava_desktop tests

.PHONY: test
test:
	poetry run pytest
