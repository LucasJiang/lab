import hashlib
from sqlalchemy.orm import load_only
from app.base.request_handler_base import RequestHandlerBase
from app.base.url_param import PA_REDIRECTED_FROM
from app.dashboard.urls import DASHBOARD_URL
from app.login.templates import LOGIN_DIR_NAME
from app.login.url_param import LOGIN_URL, PA_PASSWORD, PA_USERNAME
from app.user.models.user import User

__author__ = 'jiang'


class LoginHandler(RequestHandlerBase):
    """
    Login page
    """

    def get(self):
        self.render_template(LOGIN_DIR_NAME, 'page_login.html')

    def post(self):
        email = self.get_argument(PA_USERNAME)
        password = self.get_argument(PA_PASSWORD)
        from_url = self.get_argument(PA_REDIRECTED_FROM, '')

        password = hashlib.md5(password).hexdigest().upper()

        session = self.db_session

        user_obj = session.query(User).filter(User.email == email).options(load_only(User.name)).first()

        if not user_obj:
            self.redirect(LOGIN_URL)
            return

        if from_url:
            to_url = from_url
        else:
            to_url = DASHBOARD_URL

        self.redirect(to_url)
