web gunicorn backend.wsgi
release: python manage.py makemigrations
release python manage.py migrate
release python manage.py loaddata data.json
release pip install spacy
release python -m spacy download en_core_web_md
