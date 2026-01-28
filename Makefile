APP = restapi

test:
	python -m flake8 . --exclude .venv
	pytest -v --disable-warnings

compose:
	docker-compose build
	docker-compose up