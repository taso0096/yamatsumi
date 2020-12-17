FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /opt/yamatsumi/backend
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:5000"]
