FROM python:3.6.4

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

CMD ["uwsgi", "--ini", "uwsgi.ini:${UWSGI_ENV}"]

# RUN pip install newrelic
# ENV NEW_RELIC_ENVIRONMENT ${UWSGI_ENV}
# ENV NEW_RELIC_LICENSE_KEY {{ YOUR_LICENSE_KEY }}
# ENV NEW_RELIC_APP_NAME {{ THIS_APP_NAME }}
# CMD ["newrelic-admin", "run-program", "uwsgi", "--ini", "uwsgi.ini:${UWSGI_ENV}"]
