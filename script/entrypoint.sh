#!/bin/bash
set -e

echo "Script is executing"

if [ -e "/opt/airflow/requirements.txt" ]; then
  $(command -v python3) -m pip install --upgrade pip
  $(command -v pip3) install --user -r /opt/airflow/requirements.txt
fi

if [ ! -f "/opt/airflow/airflow.db" ]; then
  $(command -v airflow) db init && \
  $(command -v airflow) users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com \
    --password admin
fi

$(command -v airflow) db upgrade

exec $(command -v airflow) webserver
