from app.base.request_handler_base import RequestHandlerBase
from app.user.models.user import User

__author__ = 'jiang'


class DashboardHandler(RequestHandlerBase):
    """
    Home page
    """

    def get(self):
        session = self.db_session
        query_obj = session.query(User).first()
        if query_obj:
            self.write(query_obj.name + str(query_obj.id))
        else:
            obj = User(name="jiang", email="test@test.com")
            session.add(obj)
            session.commit()
            self.write(obj.name + "Hello, world")
