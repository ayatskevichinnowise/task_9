FROM apache/airflow:2.5.1
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ENV FILE_NAME "/data.csv"
ENV RAW_FILE "/data/data.csv"
ENV FILE_PATH_BAD "/data/bad"
ENV FILE_PATH_GOOD "/data/good"
ENV ERROR_LIST "/errors/errors.json"
USER root
COPY entrypoint.sh /entrypoint.sh
COPY /errors/errors.json /errors/errors.json
COPY /data/data.csv /data/data.csv
RUN mkdir -p /data/good
RUN mkdir -p /data/bad
RUN chmod +x /entrypoint.sh