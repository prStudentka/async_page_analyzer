env:
	test ! -f .env && cp .env.example .env

venv:
	poetry shell

install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	make install && psql -a -d $DATABASE_URL -f database.sql

redis:
	docker run -d --name=redis_page_analyzer -p 6379:6379 redis:latest

celery:
	celery -A page_analyzer.celery_config.celery_app worker --loglevel=info

beat:
	celery -A page_analyzer.celery_config.celery_app beat --loglevel=info

docker_stop:
	docker stop redis_page_analyzer

docker_del:
	docker remove -f redis_page_analyzer

redis_show_proc:
	ps aux | grep redis
