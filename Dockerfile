FROM python:3.6-alpine

ENV PYTHONBUFFERED 1

RUN mkdir /testappfollow_code
WORKDIR /testappfollow_code
COPY . /testappfollow_code

RUN apk add --no-cache screen postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

CMD /testappfollow_code/start.sh