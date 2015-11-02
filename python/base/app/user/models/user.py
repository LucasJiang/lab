from sqlalchemy import Column, Integer, String
from app.database.session_maker import DeclarativeBase

__author__ = 'jiang'


class User(DeclarativeBase):
    __tablename__ = 'user'
    # __table_args__ = {
    # }

    id = Column(Integer,
                primary_key=True,
                autoincrement=True
                )

    email = Column(String(30)
                   )
    
    name = Column(String(30)
                  )
