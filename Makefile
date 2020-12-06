.PHONY: run
run:
	poetry run python3 fava_desktop/main.py

.PHONY: clean
clean:
	poetry run pyclean .

.PHONY: test
test:
	poetry run pytest
