APP = restapi

test:
	python -m flake8 . --exclude .venv

compose:
	docker-compose build
	docker-compose up