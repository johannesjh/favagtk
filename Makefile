.PHONY: all
all: clean dist

.PHONY: clean
clean:
	-pyclean fava_gtk tests
	rm -rf .pytest_cache __pycache__ *.egg-info build dist venv

.PHONY: venv
venv: venv/updated

venv/updated: requirements/dev.txt
	# create a virtual environment if it does not yet exist:
	test -d venv || virtualenv -p python3 --system-site-packages venv

	# install version-locked dev dependencies in the venv:
	venv/bin/pip install --ignore-installed -r requirements/dev.txt

	# then install ourselves in editable mode.
	# without pep517 as a workaround for https://github.com/pypa/pip/issues/6264
	venv/bin/pip install --no-use-pep517 --editable .

	# update timestamp so the makefile knows that the venv has been updated:
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
