from contextlib import contextmanager

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

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


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address


User.addresses = relationship("Address", order_by=Address.id, back_populates="user")
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
    jack = User(name='jack', fullname='Jack Bean', nickname='gjffdd')
    print(jack.addresses)  # []

    jack.addresses = [
        Address(email_address='jack@google.com'),
        Address(email_address='j25@yahoo.com')]
    session.add(jack)
    print(jack.addresses[1].user)

    for u, a in session.query(User, Address).\
                        filter(User.id == Address.user_id).\
                        filter(Address.email_address == 'jack@google.com').all():
        print(u)
        print(a)

    print(session.query(User).join(Address, User.id == Address.user_id).all())  # explicit condition
    print(session.query(User).join(User.addresses).all())  # specify relationship from left to right
    print(session.query(User).join(Address, User.addresses).all())  # same, with explicit target
    print(session.query(User).join('addresses').all())  # same, using a string


