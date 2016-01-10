web: gunicorn config.wsgi:application
worker: celery worker --app=football_tools.taskapp --loglevel=info
