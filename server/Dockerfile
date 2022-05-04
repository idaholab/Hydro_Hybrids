FROM python:latest

WORKDIR  /usr/src/server

COPY . .

RUN chmod +x celery.sh
RUN apt-get update && apt-get -y upgrade
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

ENTRYPOINT /bin/bash ./entrypoint.sh
