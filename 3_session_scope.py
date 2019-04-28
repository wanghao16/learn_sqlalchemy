from contextlib import contextmanager

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String

engine = create_engine('sqlite:///:memory:')
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

Base.metadata.create_all(engine)


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


try:
    with session_scope(engine) as session:
        ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
        session.add(ed_user)
        session.commit()
        print(session.query(User).all())

        # rollback
        ed_user.name = 'Edwardo'
        print(session.query(User).all())
        raise
except:
    pass

with session_scope(engine) as session:
    print(session.query(User).all())
