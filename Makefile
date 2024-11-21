install:
	poetry install

update:
	poetry update

lint:
	poetry run flake8 .

.PHONY: run

run:
	python3 main.py
