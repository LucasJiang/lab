from datetime import datetime
from sqlalchemy import Index, Column, BIGINT, INTEGER, VARCHAR, CHAR, SMALLINT, TEXT, DATETIME
from app.database.session_maker import DeclarativeBase

__author__ = 'jiang'


class ErrorLog500(DeclarativeBase):
    __tablename__ = 'errorlog500'
    __table_args__ = (
        Index('ix_errorlog500__create_time', 'create_time'),
    )

    id = Column(INTEGER,
                primary_key=True,
                autoincrement=True
                )

    user_id = Column(INTEGER,
                     )

    user_ip = Column(VARCHAR(length=15),
                     )

    agent = Column(VARCHAR(length=200),
                   )

    method = Column(CHAR(length=1),
                    )

    code = Column(SMALLINT
                  )

    url = Column(VARCHAR(length=1000),
                 )

    args = Column(TEXT
                  )

    headers = Column(TEXT
                     )

    info = Column(TEXT
                  )

    create_time = Column(DATETIME,
                         default=datetime.utcnow(),
                         )


class ErrorLog400(DeclarativeBase):
    __tablename__ = 'errorlog400'
    __table_args__ = (
        Index('ix_errorlog400__create_time', 'create_time'),
    )

    id = Column(INTEGER,
                primary_key=True,
                autoincrement=True
                )

    user_id = Column(INTEGER,
                     )

    user_ip = Column(VARCHAR(length=15),
                     )

    agent = Column(VARCHAR(length=200),
                   )

    method = Column(CHAR(length=1),
                    )

    code = Column(SMALLINT
                  )

    url = Column(VARCHAR(length=1000),
                 )

    args = Column(TEXT
                  )

    headers = Column(TEXT
                     )

    info = Column(TEXT
                  )

    create_time = Column(DATETIME,
                         default=datetime.utcnow(),
                         )

class ErrorLog300(DeclarativeBase):
    __tablename__ = 'errorlog300'
    __table_args__ = (
        Index('ix_errorlog300__create_time', 'create_time'),
    )

    id = Column(INTEGER,
                primary_key=True,
                autoincrement=True
                )

    user_id = Column(INTEGER,
                     )

    user_ip = Column(VARCHAR(length=15),
                     )

    agent = Column(VARCHAR(length=200),
                   )

    method = Column(CHAR(length=1),
                    )

    code = Column(SMALLINT
                  )

    url = Column(VARCHAR(length=1000),
                 )

    args = Column(TEXT
                  )

    headers = Column(TEXT
                     )

    info = Column(TEXT
                  )

    create_time = Column(DATETIME,
                         default=datetime.utcnow(),
                         )

class LoggableError(Exception):
    def __init__(self, code=None, table=None):
        self.code = code

        self.table = table

    def __str__(self):
        return 'code={}'.format(self.code)
