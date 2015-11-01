from sqlalchemy import Column, Integer, String
from app.database.session_maker import DeclarativeBase

__author__ = 'jiang'


class Dashboard(DeclarativeBase):
    __tablename__ = 'dashboard'
    # __table_args__ = {
    # }

    id = Column(Integer,
                primary_key=True,
                autoincrement=True
                )

    name = Column(String(30)
                  )
