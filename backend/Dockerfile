FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /opt/yamatsumi/backend
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
