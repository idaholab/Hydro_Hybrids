FROM python:3.6.8

WORKDIR  /usr/src/server

COPY . .

RUN chmod +x celery.sh

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

ENTRYPOINT /bin/bash ./entrypoint.sh