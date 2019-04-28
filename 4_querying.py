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


with session_scope(engine) as session:
    session.add_all([
        User(name='ed', fullname='Ed Jones', nickname='edsnickname'),
        User(name='wendy', fullname='Wendy Williams', nickname='windy'),
        User(name='mary', fullname='Mary Contrary', nickname='mary'),
        User(name='fred', fullname='Fred Flintstone', nickname='freddy')])

    print(session.query(User).filter(User.name == 'ed').count())
    print(session.query(User).filter(User.name == 'ed').all())
    print(session.query(User).filter(User.name != 'ed').all())
    print(session.query(User).filter(User.name.like('%ed%')).all())
    print(session.query(User).filter(User.name != None).all())
    print(session.query(User).filter(~User.name.in_(['ed', 'wendy'])).all())

    print(session.query(User).filter(
        User.name == 'ed',
        User.fullname == 'Ed Jones').all())
    print(session.query(User)
          .filter(User.name == 'ed')
          .filter(User.fullname == 'Ed Jones').all())


