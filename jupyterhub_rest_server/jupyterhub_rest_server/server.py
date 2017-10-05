import os
from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import tornado.web
from tornado.log import enable_pretty_logging
import socket
from . import handlers as resthandlers

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

def main():

    app = Application()
    http_server = tornado.httpserver.HTTPServer(app, ssl_options={
        "certfile": "/etc/ssl/certs/cuahsi.org/cuahsi.cer",
        "keyfile": "/etc/ssl/certs/cuahsi.org/cuahsi.key"
    })
    http_server.listen(8080)
    #app.listen(os.environ['JUPYTER_REST_PORT'])
    print('\n'+'-'*60)
    print('JupyterHub REST server listening on %s:%s' % (os.environ['JUPYTER_REST_IP'],os.environ['JUPYTER_REST_PORT']))
    print('-'*60+'\n')
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
