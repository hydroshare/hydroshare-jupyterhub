from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import tornado.web
import handlers as resthandlers


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/?", resthandlers.MainHandler),
            (r"/jupyter/?",resthandlers.JupyterHandler)
        ]
        tornado.web.Application.__init__(self, handlers, debug=True)

def main():
    app = Application()
    app.listen(8080)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
