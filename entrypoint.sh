#!/bin/sh

airflow initdb
airflow users create \
    --username admin \
    --password admin \
    --firstname Firstname \
    --lastname Lastname \
    --role Admin \
    --email email@example.com

airflow webserver -dp 8080 &
airflow scheduler -d