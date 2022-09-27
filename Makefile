install:
	pip install poetry
	poetry install

mypy:
	poetry run mypy *.py

pytest:
	poetry run pytest
