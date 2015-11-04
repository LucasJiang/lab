from app.login.url_param import LOGIN_URL
from app.login.views.login import LoginHandler

__author__ = 'jiang'



LOGIN_ROUTES = [
    (LOGIN_URL, LoginHandler),
]

