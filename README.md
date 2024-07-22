# Asynchronous page-analyzer
# About
Service for checking URLs

![Homepage](https://github.com/prStudentka/hexlet-git/blob/main/pr83/flask.jpg?raw=true)

     Image 1 - Homepage Page-analyzer

# System requirements
- python = "^3.10"
- flask = "^2.3.3"
- python-dotenv = "^1.0.0"
- flake8 = "^6.1.0"
- psycopg2-binary = "^2.9.9"
- validators = "^0.22.0"
- requests = "^2.31.0"
- beautifulsoup4 = "^4.12.2"
- gunicorn = "^20.1.0"
- poetry = "^1.6.1"
- postgreSQL = "^15.0"
- celery = "^5.4.0"
- redis = "^5.0.7"

# Install
1) git clone [Repository](https://github.com/prStudentka/async_page_analyzer)
2) make install
3) created in the root directory of the project ".env" with variables:
   / создать в проекте файл ".env" c переменными:/
   - SECRET_KEY
   - DATABASE_URL
   - REDIS_URL
5) make start
