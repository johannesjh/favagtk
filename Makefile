.PHONY: all
all: clean dist

.PHONY: clean
clean:
	-pyclean fava_gtk tests
	rm -rf .pytest_cache __pycache__ *.egg-info build dist venv

.PHONY: venv
venv: venv/updated

venv/updated: requirements/env-dev.txt
	# create a virtual environment if it does not yet exist:
	test -d venv || virtualenv -p python3 --system-site-packages venv

	# for those dependecies that are easy to install in a venv,
	# ignore existing site packages and install version-locked dependencies in the venv:
	venv/bin/pip install --ignore-installed -r requirements/env-dev.txt

	# then install ourselves in editable mode.
	# it may be the case that system dependencies like PyGObject are not installed in the venv,
	# in this case, they will be accessed from system-wide site packages.
	venv/bin/pip install --editable .[all]

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
