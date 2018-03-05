FROM cuahsi/singleuser:latest

RUN mkdir -p /home/jovyan/libs/python
RUN mkdir -p /home/jovyan/sample_data
ENV PYTHONPATH="/home/jovyan/libs/python:${PYTHONPATH}"


