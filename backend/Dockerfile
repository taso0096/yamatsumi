FROM python:3

ENV PYTHONUNBUFFERED 1

RUN apt-get dist-upgrade
RUN apt-get update
RUN apt-get install build-essential
RUN apt-get install -y libgraphviz-dev graphviz pkg-config

WORKDIR /opt/yamatsumi/backend
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
