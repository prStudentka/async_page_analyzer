import requests
from page_analyzer import _utils
from flask import Flask, redirect, request, render_template, flash, get_flashed_messages, url_for, g
from os import getenv
from dotenv import load_dotenv
from page_analyzer import model
from page_analyzer.tasks import check_urls_task


load_dotenv()
__DATABASE_URL = getenv('DATABASE_URL')
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')


def get_connection():
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = model.create_conn(__DATABASE_URL)
    return conn


@app.teardown_appcontext
def close_connection(exception):
    conn = getattr(g, '_database', None)
    if conn is not None:
        model.close_conn(conn)


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


@app.post('/urls')
def post_page():
    url = request.form.get('url')
    error = _utils.validate_url(url)
    if error:
        flash(error, 'danger')
        return render_template('index.html', messages=error), 422
    url_name = _utils.get_clean_url(url)
    conn = get_connection()
    res_check = model.check_url(conn, url_name)
    if not res_check:
        res_check = model.add_url(conn, url_name)
        flash('Страница успешно добавлена', 'success')
    else:
        flash('Страница уже существует', 'info')
    return redirect(url_for('url_id', id=res_check.id))


@app.get('/urls')
def get_urls():
    messages = get_flashed_messages(with_categories=True)
    content = model.get_urls_with_checks(get_connection())
    return render_template('/urls.html', content=content,
                           messages=messages)


@app.get('/urls/<int:id>')
def url_id(id):
    messages = get_flashed_messages(with_categories=True)
    conn = get_connection()
    checks = model.get_checks(conn, id)
    content = model.get_url(conn, id)
    return render_template('/url.html', content=content,
                           test=checks, messages=messages)


@app.post('/urls/<id>/checks')
def process_checks_id(id):
    url = model.get_url(get_connection(), id)
    try:
        response = requests.get(url.name)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
    else:
        page_data = _utils.get_parse_html(response)
        page_data['id'] = id
        model.create_check(get_connection(), page_data)
        flash('Страница успешно проверена', 'success')
    finally:
        return redirect(url_for('url_id', id=id))


@app.post('/urls/checks')
def process_urls_check():
    check_urls_task.delay()
    flash('Процесс проверки всех страниц запущен','success')
    return redirect(url_for('get_urls'))
