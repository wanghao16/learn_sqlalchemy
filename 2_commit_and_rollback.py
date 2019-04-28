
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

Session = sessionmaker(bind=engine)  # autocommit=False

# commit
session = Session()
ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
session.add(ed_user)
session.commit()
print(session.query(User).all())

# rollback
ed_user.name = 'Edwardo'
print(session.query(User).all())
session.rollback()
print(session.query(User).all())
