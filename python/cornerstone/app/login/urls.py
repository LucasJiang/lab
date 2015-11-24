from app.login.url_param import LOGIN_URL, API_LOGOUT
from app.login.views.login import PageLoginHandler, API_LogoutHandler

__author__ = 'jiang'



LOGIN_ROUTES = [
    (LOGIN_URL, PageLoginHandler),
    (API_LOGOUT, API_LogoutHandler),
]

