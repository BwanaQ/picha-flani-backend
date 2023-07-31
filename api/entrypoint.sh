#!/bin/sh

# Check if migrations are required
if python manage.py makemigrations --check --noinput; then
  # Apply migrations if needed
  python manage.py migrate --noinput
else
  echo "No new migrations found. Skipping migration step."
fi

# Check if static files need to be collected
if python manage.py collectstatic --dry-run --noinput; then
  # Collect static files if needed
  python manage.py collectstatic --noinput
else
  echo "No new static files found. Skipping collectstatic step."
fi

# Start the web application
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000