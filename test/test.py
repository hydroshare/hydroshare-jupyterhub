import tornado.ioloop
import tornado.web
import socket
from tornado.log import enable_pretty_logging

enable_pretty_logging()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        base = socket.gethostbyname(socket.gethostname())
        self.render('index.html', message='',ip=base, username='', restype='', resid='')


class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument('username', '')
        restype = self.get_argument('restype', '')
        resid = self.get_argument('resid', '')
        message = ''
        error = False
        if not username:
            msg = 'Please enter your JupyterHub Username.'
            error = True
        elif not restype:
            msg = 'Please enter the HydroShare resource type.'
            error = True
        elif not resid:
            msg = 'Please enter the HydroShare resource ID.'
            error = True
        if error: 
            self.render('index.html', message=msg, ip=base, username=username, restype=restype, resid=resid)
        else:
            base = socket.gethostbyname(socket.gethostname())
            jhub_addr = 'http://%s:8080/jupyter?username=%s&resourcetype=%s&resourceid=%s' % (base, username, restype, resid)
            self.redirect(jhub_addr, status=303)
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)

    # print some info to the terminal
    print('\nTornado web server running on %s:8888\n' % (socket.gethostbyname(socket.gethostname())))

    tornado.ioloop.IOLoop.current().start()



