#!/usr/bin/env bash

while ! /usr/bin/pg_isready -h $DB_HOST -p ${DB_PORT:-5432} > /dev/null 2> /dev/null; do
    echo "Connecting DB (Host: $DB_HOST, port: ${DB_PORT:-5432})"
    sleep 1
  done

echo "DB UP, connecting in 3 sec"
sleep 3

alembic upgrade head &&
python run_server.py
