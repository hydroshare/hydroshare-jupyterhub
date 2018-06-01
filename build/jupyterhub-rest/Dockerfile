FROM ubuntu:xenial

MAINTAINER Tony Castronova <acastronova@cuahsi.org>


ADD install-deps.sh /tmp/install-deps.sh
#ADD utilities.py /tmp/utilities.py
RUN sh /tmp/install-deps.sh

RUN mkdir /app
WORKDIR /app 
ADD start.py /app/start.py

ENTRYPOINT python3 start.py


