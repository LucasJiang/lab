from tornado.web import RequestHandler

__author__ = 'jiang'


class PageNotFoundHandler(RequestHandler):
    """
    404 Page
    """
    def data_received(self, chunk):
        pass

    def get(self):
        self.write("404, page not found")


class PageError500Handler(RequestHandler):
    """
    500 Page
    """
    def data_received(self, chunk):
        pass

    def get(self):
        self.write("500, server error")
