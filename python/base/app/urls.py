from app.dashboard.urls import DASHBOARD_ROUTES
from app.exception.exception_handler import PageNotFoundHandler
from app.settings_init import SITE_URL, SITE_URL_LEN, SITE_URL_HTTPS, SITE_URL_HTTPS_LEN

__author__ = 'jiang'


def remove_scheme_and_host_from_routes(routes, add_ending_dollar=False):
    new_routes = []

    for route_info_tuple in routes:

        pattern = route_info_tuple[0]

        if pattern.startswith(SITE_URL):
            new_pattern = pattern[SITE_URL_LEN:]
        elif pattern.startswith(SITE_URL_HTTPS):
            new_pattern = pattern[SITE_URL_HTTPS_LEN:]
        else:
            new_pattern = pattern

        if add_ending_dollar:
            if new_pattern[-1] != '$':
                new_pattern += '$'

        new_route_info_list = [new_pattern]
        new_route_info_list.extend(route_info_tuple[1:])

        new_route_info_tuple = tuple(new_route_info_list)

        new_routes.append(new_route_info_tuple)

    return new_routes


ROUTES = DASHBOARD_ROUTES + \
    [('.*', PageNotFoundHandler)]
ROUTES = remove_scheme_and_host_from_routes(ROUTES, add_ending_dollar=True)
