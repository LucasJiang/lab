from app.database.declarative_base import DeclarativeBase

__author__ = 'jiang'


def create_init_data(engine):
    # import model to create table
    from app.dashboard.models import dashboard

    DeclarativeBase.metadata.create_all(engine)
