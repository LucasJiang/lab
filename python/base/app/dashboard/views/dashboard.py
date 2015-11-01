from tornado.web import RequestHandler
from app.base.request_handler_base import RequestHandlerBase
from app.dashboard.models.dashboard import Dashboard

__author__ = 'jiang'


class DashboardHandler(RequestHandlerBase):
    """
    Home page
    """

    def get(self):
        session = self.get_session()
        query_obj = session.query(Dashboard).first()
        if query_obj:
            self.write(query_obj.name+str(query_obj.id))
        else:
            obj = Dashboard(name="jiang")
            session.add(obj)
            session.commit()
            self.write(query_obj.name+"Hello, world")
