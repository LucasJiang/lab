from app.login.views.login import LoginHandler

__author__ = 'jiang'


LOGIN_URL = '/login'

DASHBOARD_ROUTES = [
    (LOGIN_URL, LoginHandler),
]
