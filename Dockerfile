FROM python:3.10
COPY requirements.txt requirements.txt
ENV FILE_PATH "/data"
ENV FILE_NAME "/data.csv"
ENV FILE_PATH_BAD "/data/bad"
ENV FILE_PATH_GOOD "/data/good"
ENV ERROR_LIST "/errors/errors.json"
ENV EMAIL "alexander.yatskevich@innowise-group.com"
RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]