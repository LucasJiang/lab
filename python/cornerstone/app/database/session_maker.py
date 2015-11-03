from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import settings_init
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'jiang'

# use settings_init.SQL_ENGINE instand of SQL_ENGINE ,becasue set settings obj
ENGINE = create_engine(settings_init.SQL_ENGINE, echo=True)

DeclarativeBase = declarative_base()

def get_new_session():
    print(settings_init.SQL_ENGINE)
    return sessionmaker(bind=ENGINE)()
