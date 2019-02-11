import os
from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import tornado.web
from tornado.log import enable_pretty_logging
import socket
from . import handlers as resthandlers
from . import settings as Settings

enable_pretty_logging()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/jupyter/?",resthandlers.JupyterHandler),
            (r"/",resthandlers.IndexHandler)
        ]
        settings = {
            "debug":True,
            "login_url":os.path.join(os.environ['JUPYTER_REST_IP'], ':%s' % os.environ['JUPYTER_PORT']),
	    "template_path":Settings.TEMPLATE_PATH,
	    "static_path":Settings.STATIC_PATH,
        }
        tornado.web.Application.__init__(self, handlers, **settings)

def main():

    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)

    cert = os.environ.get('SSL_CERT', None)
    key = os.environ.get('SSL_KEY', None)
    if (cert is not None) and (key is not None):
        ssl_options={
            "certfile": cert,
            "keyfile": key
        })

    http_server.listen(8080)
    #app.listen(os.environ['JUPYTER_REST_PORT'])
    print('\n'+'-'*60)
    print('JupyterHub REST server listening on %s:%s' % (os.environ['JUPYTER_REST_IP'],os.environ['JUPYTER_REST_PORT']))
    print('-'*60+'\n')
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
