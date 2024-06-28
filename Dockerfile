FROM python:3.6.1-alpine

WORKDIR /app

ADD . /app

RUN apt-get update
RUN apt-get upgrade
RUN apt-get install python-pip
RUN pip3 install flask
RUN pip3 install mysql.connector

CMD ["python3","web_01_v2.py"]
