#!/bin/sh
manage=/app/manage.py
# Make migrations.
echo "Making migrations..." &&
python $manage makemigrations --noinput &&
# Run migrations.
echo "Running migration..." &&
python $manage migrate --noinput &&
# Run server.
echo "Running server..." &&
python $manage runserver 0.0.0.0:8000