from app.database.session_maker import ENGINE, DeclarativeBase
from exts.copy_setttings import set_setting_obj

__author__ = 'jiang'

def main():
    set_setting_obj()
    create_init_data(ENGINE)


def create_init_data(engine):
    """import model to create table"""

    from app.user.models import user
    from app.exception.models import error_log

    DeclarativeBase.metadata.create_all(engine)


if __name__ == '__main__':
    main()
