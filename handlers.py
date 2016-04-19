
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name', default=None, strip=True)
        if name is None:
            self.write('missing parameter: "name"')
            return

        self.write('Hello %s'%name)


class JupyterHandler(tornado.web.RequestHandler):
    def get(self):
        notebook = self.get_argument('notebook', default=None, strip=True)
        if notebook is None:
            self.write('missing parameter: "notebook"')
            return
        self.redirect("http://129.123.51.34/user/tony/notebooks/demos.ipynb")
        #self.write('Redirect to notebook %s'%notebook)



