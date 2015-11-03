from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship
from app.database.session_maker import DeclarativeBase
from app.user.models.user import User

__author__ = 'jiang'


class Address(DeclarativeBase):
    __tablename__ = 'address'
    # __table_args__ = {
    # }

    id = Column(Integer,
                primary_key=True,
                autoincrement=True
                )

    address = Column(String(200)
                     )

    name = Column(String(100)
                  )

    user_id = Column(Integer,
                     ForeignKey(User.id)
                     )

    # many to one /meanwhile if add backref == add one to many
    user_obj = relationship(User, backref=backref('address_obj_s', order_by=id))
