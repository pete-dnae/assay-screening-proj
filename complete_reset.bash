#!/bin/bash

# Make sure the script gets run in the same directory as the script itself.
SCRIPT_PATH=${0%/*}
cd ${SCRIPT_PATH}

# Remove the existing database and migration files if there are any.
rm db.sqlite3
rm -rf app/migrations

# Make the Django migrations and run them to create the db and tables.
python manage.py makemigrations app
python manage.py migrate

# Create an admin user called admin with password fibble.
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'fibble')" | python manage.py shell

# Populate the database with the starter content - i.e reference experiement.
python manage.py reset_db
