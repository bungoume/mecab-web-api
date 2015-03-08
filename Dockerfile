FROM python:3.4.3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN \
  apt-get update -qq && \
  apt-get install -qq libmecab-dev && \
  apt-get install -qq mecab mecab-ipadic-utf8

RUN pip install uWSGI
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app

CMD ["uwsgi", "uwsgi.ini"]
