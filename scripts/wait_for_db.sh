#!/bin/sh

set -e

# Wait for the database to be ready
/wait_for_db.sh

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Start the app
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
