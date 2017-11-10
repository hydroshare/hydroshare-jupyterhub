FROM python:2.7
ADD requirements.txt /app/requirements.txt
ADD ./celeryworker/ /app/
WORKDIR /app/
RUN pip install -r requirements.txt

# add docker-cli
RUN wget https://download.docker.com/linux/static/stable/x86_64/docker-17.09.0-ce.tgz \
 && tar -xf docker-17.09.0-ce.tgz \
 && cp docker/docker /usr/bin/docker

ENTRYPOINT celery -A celeryworker worker --loglevel=info
