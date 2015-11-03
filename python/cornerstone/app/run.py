from app.urls import ROUTES
import tornado.ioloop
import tornado.web
from app import settings_init
from exts.copy_setttings import set_setting_obj

__author__ = 'jiang'


set_setting_obj()
application = tornado.web.Application(ROUTES)

def main():
    """
    Main     start
    :option: -c "conf path"
    """
    # start app
    application.listen(settings_init.SITE_PORT)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()