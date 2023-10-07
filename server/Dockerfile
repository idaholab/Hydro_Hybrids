FROM python:3.10

WORKDIR  /usr/src/server

COPY . .
RUN chmod +x celery.sh
RUN apt-get update && apt-get -y upgrade

RUN pip config set global.trusted-host \
    "pypi.org files.pythonhosted.org pypi.python.org" \
    --trusted-host=pypi.python.org \
    --trusted-host=pypi.org \
    --trusted-host=files.pythonhosted.org
RUN pip3 install -r requirements.dev.txt
RUN pip3 install gunicorn

ENTRYPOINT /bin/bash ./entrypoint.sh
