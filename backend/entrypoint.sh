#!/bin/sh

echo "MySQL is not started yet..."

# check host and port access
while ! nc -z db 3306; do
  sleep 1
done

sleep 5

echo "MySQL is started"

cd ./app || true
python manage.py makemigrations --noinput
python manage.py migrate --noinput

python manage.py loaddata equipment_app/fixtures/initial_data.json

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL"
    python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
user = User.objects.get(username='$DJANGO_SUPERUSER_USERNAME');
user.set_password('$DJANGO_SUPERUSER_PASSWORD');
user.save();
"
fi

exec gunicorn --bind 0.0.0.0:8000 core.wsgi:application