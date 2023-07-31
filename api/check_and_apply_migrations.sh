#!/bin/bash

# Check for pending migrations
echo "Checking for pending migrations..."
python manage.py makemigrations --check --dry-run > /dev/null

if [[ $? -eq 0 ]]; then
  echo "Applying migrations..."
  python manage.py migrate
else
  echo "No pending migrations found."
fi