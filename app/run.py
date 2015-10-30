from sqlalchemy import create_engine
from app.database.data_init import create_init_data
from app.urls import ROUTES
import getopt
import sys
import os
import tornado.ioloop
import tornado.web
from app import settings_init
from exts.copy_setttings import copy_settings
from exts.module import import_module_by_path, find_module

__author__ = 'jiang'


def set_setting_obj():
    """
    set setting obj from -c or from settings.py and settings_init.py
    """
    #getopt.getopt(sys.argv[1:],"hp:i:",["help","ip=","port="])
    opts, args = getopt.getopt(sys.argv[1:], "c:d:")
    specified_path = None
    for opt, value in opts:
        #conf file instead but 
        if opt == "-c" and os.path.exists(value):
            specified_path = value
    current_path = sys.path[0]
    settings_path = os.path.join(current_path, "settings") if not specified_path else specified_path
    src_module_obj = import_module_by_path(settings_path)

    # must use find module ,then ,after copy settings ,refresh in cache
    dest_module_obj = find_module("app.settings_init")
    copy_settings(src_module_obj, dest_module_obj)


set_setting_obj()
application = tornado.web.Application(ROUTES)

# use settings_init.SQL_ENGINE instand of SQL_ENGINE ,becasue set settings obj
ENGINE = create_engine(settings_init.SQL_ENGINE, echo=True)

def main():
    """
    Main     start
    :option: -c "conf path"
    """
    # create table
    # if s
    create_init_data(ENGINE)
    print()
    # start app
    application.listen(settings_init.SITE_PORT)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
