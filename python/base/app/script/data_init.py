from app.database.declarative_base import DeclarativeBase
from app.run import ENGINE
from exts.copy_setttings import set_setting_obj

__author__ = 'jiang'

def main():
    set_setting_obj()
    create_init_data(ENGINE)


def create_init_data(engine):
    """import model to create table"""

    from app.dashboard.models import dashboard

    DeclarativeBase.metadata.create_all(engine)


if __name__ == '__main__':
    main()
