FROM jupyterhub/jupyterhub:latest
MAINTAINER Tony Castronova <acastronova@cuahsi.org>

ADD install-deps.sh /tmp/install-deps.sh
RUN sh /tmp/install-deps.sh

ADD cull_idle_servers.py /srv/cull_idle_servers.py
