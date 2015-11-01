from tornado.web import RequestHandler
from app.database.session_maker import get_new_session

__author__ = 'jiang'


class RequestHandlerBase(RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        self.db_session = None
        RequestHandler.__init__(self, application, request, **kwargs)

    def get_session(self):
        if not self.db_session:
            self.db_session = get_new_session()
        return self.db_session

