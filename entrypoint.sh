#!/bin/sh

# Wait for the database to be ready before applying migrations
./wait-for-it.sh db:5432 -- echo "Database is up - continuing..."

# Apply database migrations
alembic upgrade head
