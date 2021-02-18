.PHONY: all
all: clean dist

.PHONY: clean
clean:
	-pyclean fava_gtk tests
	rm -rf .pytest_cache __pycache__ *.egg-info build dist venv

.PHONY: requirements
requirements:
	pip-compile-multi

requirements/%.txt: requirements/%.in $(wildcard requirements/*.in)
	pip-compile-multi --use-cache -t $<

.PHONY: venv
venv: venv/updated

venv/updated: requirements/env-dev.txt
	test -d venv || virtualenv -p python3 --system-site-packages venv
	venv/bin/pip install --ignore-installed -c requirements/env-dev.txt --editable .[all]
	touch venv/updated

.PHONY: run
run: venv/updated
	venv/bin/python fava_gtk/main.py

.PHONY: test
test:
	venv/bin/pytest ./tests

.PHONY: dist
dist:
	python3 setup.py bdist_wheel
