FROM python:3.6.8

RUN pip install --upgrade pip

# RUN apt-get update

# RUN apt-get install acl

WORKDIR /usr/src/server

COPY . .

RUN pip install -r requirements.txt
