import os

SITE_HOST = '127.0.0.1'
SITE_PORT = 8888
SITE_HOST_HTTPS = None
SITE_PORT_HTTPS = 443



SQL_ENGINE = 'sqlite:///backend.db'


PROJECT_SRC_DIR = os.path.dirname(__file__)

if SITE_HOST_HTTPS is None:
    SITE_HOST_HTTPS = SITE_HOST

if SITE_PORT is None or SITE_PORT == 80:
    SITE_SERVER = SITE_HOST
else:
    SITE_SERVER = '{}:{}'.format(SITE_HOST, SITE_PORT)

if SITE_PORT_HTTPS is None or SITE_PORT_HTTPS == 443:
    SITE_SERVER_HTTPS = SITE_HOST_HTTPS
else:
    SITE_SERVER_HTTPS = '{}:{}'.format(SITE_HOST_HTTPS, SITE_PORT_HTTPS)

# site url
SITE_URL = 'http://{}'.format(SITE_SERVER)
SITE_URL_LEN = len(SITE_URL)

# site url https
SITE_URL_HTTPS = 'https://{}'.format(SITE_SERVER_HTTPS)
SITE_URL_HTTPS_LEN = len(SITE_URL_HTTPS)
