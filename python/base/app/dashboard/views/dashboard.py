from sqlalchemy.orm import load_only, subqueryload, defer, lazyload
from app.base.request_handler_base import RequestHandlerBase
from app.user.models.address import Address
from app.user.models.user import User

__author__ = 'jiang'


class DashboardHandler(RequestHandlerBase):
    """
    Home page
    """

    def get(self):
        session = self.db_session
        # query demo
        user_obj = session.query(User)\
            .options(defer(User.email), lazyload("address_obj_s").load_only("name")).first()
        if user_obj:
            self.render_dashboard_template('page_dashboard.html', name=user_obj.name,
                                           address_obj_s=user_obj.address_obj_s)
        else:
            obj = User(name="jiang", email="test@test.com")
            session.add(obj)
            session.flush()
            address_1 = Address(name="address name 1", address="Rd 1", user_id=obj.id)
            address_2 = Address(name="address name 2", address="Rd 2", user_id=obj.id)
            session.add(address_1)
            session.add(address_2)
            session.commit()
            self.write(obj.name + "Hello, world")
