from __future__ import absolute_import
from celery import Celery
import socket

# todo: these should all be environment vars
#IP = socket.gethostbyname(socket.gethostname())
IP = '10.202.2.137'
PRJ = 'celeryworker'
PORT = '5672'
RABBIT_USER = 'admin'
RABBIT_PASS = 'mypass'

app = Celery(PRJ,
             broker='amqp://%s:%s@%s:%s' % (RABBIT_USER, RABBIT_PASS,
                                            IP, PORT),
             backend='rpc://',
             include=['celeryworker.tasks'])
