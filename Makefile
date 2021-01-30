.PHONY: all
all: clean dist


null :=
space := ${null} ${null}
WHEEL = $(subst ${space},-,$(subst -,_,$(shell poetry version)))-py3-none-any.whl


.PHONY: clean
clean:
	-poetry run pyclean fava_gtk tests
	rm -rf .pytest_cache __pycache__ build dist


dist: dist/$(WHEEL) dist/requirements.txt
	touch dist/.trackerignore
	poetry run pip3 download -r dist/requirements.txt --dest dist/

dist/$(WHEEL):
	poetry build --format wheel

dist/requirements.txt:
	poetry export --without-hashes --extras all --output dist/requirements.txt


.PHONY: run
run:
	poetry run python3 fava_gtk/main.py


.PHONY: test
test:
	poetry run pytest ./tests

