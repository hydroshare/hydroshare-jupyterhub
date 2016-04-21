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
        tornado.web.Application.__init__(self, handlers, debug=True)

def main():
    app = Application()
    app.listen(8080)
    print('\n'+'-'*60)
    print('JupyterHub REST server listening on %s:8080' % socket.gethostbyname(socket.gethostname()))
    print('-'*60+'\n')
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
