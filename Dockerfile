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

RUN python text_analysis/manage.py collectstatic --noinput

EXPOSE 8000

ENV UWSGI_ENV production

CMD ["uwsgi", "--ini", uwsgi.ini:${UWSGI_ENV}"]
