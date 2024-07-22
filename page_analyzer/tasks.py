from os import getenv
import requests
from page_analyzer.celery_config import celery_app
from page_analyzer.model import create_conn, get_urls, create_check
from page_analyzer._utils import get_parse_html


DATABASE_URL = getenv('DATABASE_URL')


@celery_app.task
def check_urls_task():
    conn = create_conn(DATABASE_URL)
    urls_data = get_urls(conn)
    for url in urls_data:
        try:
            response = requests.get(url.name)
        except requests.RequestException:
            create_check(conn, {
                'id': url.id,
                'code': 0,
                'h1': '',
                'title': '',
                'description': 'Ошибка сети'
            })
            continue
        page_data = get_parse_html(response)
        page_data['id'] = url.id
        create_check(conn, page_data)
        