
FROM debian
RUN apt-get update
RUN apt-get install -y wget net-tools vim python python-pip
RUN pip install celery
WORKDIR /app
CMD ["/bin/sh"]

#RUN wget https://download.docker.com/linux/static/stable/x86_64/docker-17.09.0-ce.tgz \
# && tar -xf docker-17.09.0-ce.tgz \
# && cp docker/docker /usr/bin/docker

#RUN /bin/sh rc-update add docker boot
#RUN systemctl enable docker
#RUN systemctl start docker

