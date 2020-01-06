#!/bin/sh
echo "Removing Database"
rm db.sqlite3

echo "Migrating"
cd auction
./manage.py makemigrations
./manage.py migrate
