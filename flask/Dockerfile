FROM python:3.7.1-stretch

# Environment variables
ENV REDIS_PW = "root"
ENV MONGO_USERNAME = "root"
ENV MONGO_PASSWORD = "example"

ADD . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uwsgi", "wsgi.ini"]
