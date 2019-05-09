FROM python:3.6-alpine

ENV PYTHONBUFFERED 1

RUN mkdir /hackertest
WORKDIR /hackertest
COPY . /hackertest

RUN apk add --no-cache screen postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

CMD /hackertest/start.sh