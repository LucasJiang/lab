from app.base.url_param import DASHBOARD_URL
from app.dashboard.views.dashboard import PageDashboardHandler

__author__ = 'jiang'



DASHBOARD_ROUTES = [
    (DASHBOARD_URL, PageDashboardHandler),
]
