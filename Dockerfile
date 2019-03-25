FROM python:3.6

RUN apt-get update
RUN apt-get install screen
ENV PYTHONBUFFERED 1
RUN mkdir /hackertest
WORKDIR /hackertest
ADD requirements.txt /hackertest/
RUN pip install -r requirements.txt
ADD start.sh /hackertest/
ADD . /hackertest

CMD ["/bin/bash", "/hackertest/start.sh"]