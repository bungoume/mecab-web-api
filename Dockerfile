FROM python:3.7.0-alpine

RUN mkdir -p /usr/src/app && mkdir /log && \
    apk --no-cache --update add \
                            build-base \
                            linux-headers \
                            openssl \
                            libstdc++ \
                            bash \
                            curl \
                            file \
                            git \
                            ca-certificates && \
    cd /tmp && \
    wget -O mecab-0.996.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE" && \
    tar xvzf mecab-0.996.tar.gz && \
    cd mecab-0.996 && \
    ./configure --enable-utf8-only && \
    make && make install && \
    mkdir -p /usr/local/lib/mecab/dic && \
    chmod 777 /usr/local/lib/mecab/dic && \
    cd /tmp && \
    git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && \
    cd mecab-ipadic-neologd && \
    ./bin/install-mecab-ipadic-neologd -n -y && \
    sed -i "s/ipadic$/mecab-ipadic-neologd/g" /usr/local/etc/mecabrc && \
    pip install uWSGI mecab-python3==0.7 && \
    apk del build-base linux-headers && \
    rm -rf /tmp/* /var/tmp/* /var/cache/apk/* /root/.cache/pip/*

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /tmp/* /var/tmp/* /root/.cache/pip/*

COPY . /usr/src/app

ENV DJANGO_SETTINGS_MODULE=text_analysis.settings.production

RUN python text_analysis/manage.py collectstatic --noinput

EXPOSE 8000

ENV UWSGI_ENV production

CMD ["uwsgi", "--ini", "uwsgi.ini:${UWSGI_ENV}"]

# RUN pip install newrelic
# ENV NEW_RELIC_ENVIRONMENT ${UWSGI_ENV}
# ENV NEW_RELIC_LICENSE_KEY {{ YOUR_LICENSE_KEY }}
# ENV NEW_RELIC_APP_NAME {{ THIS_APP_NAME }}
# CMD ["newrelic-admin", "run-program", "uwsgi", "--ini", "uwsgi.ini:${UWSGI_ENV}"]
