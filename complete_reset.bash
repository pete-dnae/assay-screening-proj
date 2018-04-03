#!/bin/bash

# A script to OBLITERATE and repopulate an EXISTING database, IFF the 
# database is SQLite.

# Make sure the script gets run in the same directory as the script itself.
SCRIPT_PATH=${0%/*}
cd ${SCRIPT_PATH}

# Abort immediately if the database is not SQLite
if [ ! -e db.sqlite3 ]
then
    echo "Aborting with no changes, because could not detect db.sqlite3."
    exit
fi

# Remove the existing database and migration files if there are any.
rm db.sqlite3
rm -rf app/migrations

# Make the Django migrations and run them to create the db and tables.
python manage.py makemigrations app
python manage.py migrate

# Create an admin user called admin with password fibble.
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'fibble')" | python manage.py shell

# Further populate the database with the reference experiment.
python manage.py pop_with_ref_exp
