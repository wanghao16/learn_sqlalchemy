
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.pool import NullPool

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)


"""
DEFAULT:
pool_size=5
poolclass=sqlalchemy.pool.Pool
"""
engine = create_engine('sqlite:///:memory:', poolclass=NullPool)
Base.metadata.create_all(engine)

