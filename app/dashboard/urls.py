from app.dashboard.views.dashboard import DashboardHandler

__author__ = 'jiang'

DASHBOARD_URL = '/dashboard'

DASHBOARD_ROUTES = [
    (DASHBOARD_URL, DashboardHandler),
]
