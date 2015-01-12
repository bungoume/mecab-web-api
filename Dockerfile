FROM python:3-onbuild

RUN pip install uWSGI

CMD ["uwsgi", "uwsgi.ini"]
