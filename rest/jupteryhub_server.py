import os
from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import tornado.web
from tornado.log import enable_pretty_logging
import handlers as resthandlers
import socket

enable_pretty_logging()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/jupyter/?",resthandlers.JupyterHandler)
        ]
        settings = {
            "debug":True,
            "login_url":os.path.join(os.environ['JUPYTER_REST_IP'], ':%s' % os.environ['JUPYTER_PORT'])
#            "login_url":'http://129.123.51.34:80/',
        }
        tornado.web.Application.__init__(self, handlers, **settings)

def set_env():
    for line in open('../jupyterhub/env'):
        li = line.strip()
        if not li.startswith('#') and li != '':
            li = li.replace('export', '').strip()  # remove the export tag
            var,val = li.split('=', 1)  # split at first occurence of '='
            os.environ[var] = val

def main():
    # set environment variables
    set_env()

    app = Application()
    app.listen(os.environ['JUPYTER_REST_PORT'])
    print('\n'+'-'*60)
    print('JupyterHub REST server listening on %s:%s' % (os.environ['JUPYTER_REST_IP'],os.environ['JUPYTER_REST_PORT']))
    print('-'*60+'\n')
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
