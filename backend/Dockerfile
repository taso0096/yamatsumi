FROM python:3

ENV PYTHONUNBUFFERED 1

COPY . /opt/yamatsumi/backend
WORKDIR /opt/yamatsumi/backend

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "main.py"]
