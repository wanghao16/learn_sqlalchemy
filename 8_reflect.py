
import os
import sys
import logging
from contextlib import contextmanager

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, create_engine, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String


engine = create_engine('mysql+mysqldb://root:root@localhost/test?charset=utf8mb4')
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    fullname = Column(String(64))
    nickname = Column(String(64))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)


Base.metadata.create_all(engine)


"""
# generate sqlalchemy models:
sqlacodegen --tables users mysql+mysqldb://root:root@localhost/test?charset=utf8mb4
"""


@contextmanager
def session_scope(engine):
    """Provide a transactional scope around a series of operations."""
    sess_cls = sessionmaker(bind=engine)
    session = sess_cls()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class ReflectUser(Base):
    __table__ = Table('users', Base.metadata, autoload=True, autoload_with=engine)


with session_scope(engine) as sess:
    sess.add(User(name='ed', fullname='Ed Jones', nickname='edsnickname'))
    print sess.query(User).count()

with session_scope(engine) as sess:
    sess.add(ReflectUser(name='wendy', fullname='Wendy Williams', nickname='windy'))

with session_scope(engine) as sess:
    print sess.query(User).count()

