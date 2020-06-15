#!/bin/bash
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-pyconkr.prod-settings}
echo "Yarn install"
yarn install

echo "Collect static files"
python manage.py compilemessages
python manage.py compilescss
python manage.py collectstatic --noinput &
#python manage.py compress --force

echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

# For Debug
echo ""
echo "========== python manage.py showmigrations =========="
python manage.py showmigrations
echo ""
echo ""

echo "Create admin user"
CREATE_ADMIN_SOURCE="
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
UserModel = get_user_model()
# Create admin user
USERNAME='pyconkr'
EMAIL='pyconkr@pycon.kr'
# Should be changed
PASSWORD='pyconkr'
try:
    UserModel.objects.get(username=USERNAME)
except UserModel.DoesNotExist:
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
"
echo "${CREATE_ADMIN_SOURCE}"  | python manage.py shell

mkdir -p /logs
touch /logs/gunicorn.log
touch /logs/access.log
tail -n 0 -f /logs/*.log &

echo "==== Starting server ====="
gunicorn pyconkr.wsgi:application \
    --bind=0.0.0.0:8000 \
    --workers 1 \
#    --threads 256 \
    --worker-connections=5000 \
    --max-requests 10000 \
    --max-requests-jitter 5 \
    -k gevent \
    --log-level=info \
    --log-file=/logs/gunicorn.log \
#    --log-file=-
    --access-logfile=/logs/access.log \
#    --preload
# https://stackoverflow.com/questions/12449172/how-to-debug-gunicorn-failure-issues-worker-failed-to-boot
