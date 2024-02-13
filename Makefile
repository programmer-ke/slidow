all: test lint

test:
	pytest slidow/tests

lint: 	black isort mypy

black:
	black --check slidow

isort:
	isort --check slidow

mypy:
	mypy slidow

