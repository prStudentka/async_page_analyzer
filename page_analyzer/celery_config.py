from os import getenv
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab


load_dotenv()

CELERY_BROKER_URL = getenv('REDIS_URL')
CELERY_RESULT_BACKEND = getenv('REDIS_URL')


def make_celery():
    celery = Celery(
        main='page_analyzer',
        broker=CELERY_BROKER_URL,
        backend=CELERY_RESULT_BACKEND,
    )
    return celery


celery_app = make_celery()

celery_app.conf.beat_schedule = {
    'process_urls_checks_every_minutes': {
        'task': 'page_analyzer.tasks.check_urls_task',
        'schedule': crontab(minute='*/1'),
    },
}