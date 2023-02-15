#!/bin/bash

airflow db init
airflow users create --username admin --password admin --firstname Firstname --lastname Lastname --role Admin --email email@example.com

exec airflow webserver -p 8080 & exec airflow scheduler