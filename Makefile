install:
	poetry install

update:
	poetry update

lint:
	flake8

.PHONY: run

run:
	python3 main.py
