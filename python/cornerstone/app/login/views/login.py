from tornado.web import RequestHandler

__author__ = 'jiang'

class LoginHandler(RequestHandler):
    """
    Home page
    """
    def data_received(self, chunk):
        pass

    def get(self):
        self.write("Hello, world")
