
from app.urls import ROUTES
import tornado.ioloop
import tornado.web

__author__ = 'jiang'



application = tornado.web.Application(ROUTES)

def main():
    """
    Main     start
    :option: -c "conf path"
    """

    from exts.copy_setttings import set_setting_obj
    set_setting_obj()
    from app import settings_init
    print("Link:{}".format(settings_init.SITE_SERVER))
    # start app
    application.listen(settings_init.SITE_PORT)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
