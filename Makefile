.PHONY: build
build: fava
	poetry build

fava:
	git clone --single-branch --branch master --depth 1 https://github.com/beancount/fava.git
	make -C fava

.PHONY: run
run:
	poetry run python3 fava_desktop/main.py

.PHONY: clean
clean:
	rm -rf .pytest_cache build dist fava
	poetry run pyclean fava_desktop tests

.PHONY: test
test:
	poetry run pytest
