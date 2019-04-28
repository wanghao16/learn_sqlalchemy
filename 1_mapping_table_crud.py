
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)
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

# create tables
Base.metadata.create_all(engine)

# create a session
Session = sessionmaker(bind=engine)  # autocommit=False
session = Session()

# ORM
ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
print(ed_user.name)
print(ed_user.nickname)
print(str(ed_user.id))

# create instance
session.add(ed_user)
# update instance
ed_user.nickname = 'eddie'
session.add(ed_user)
# delete instance
session.delete(ed_user)
# insert or update
session.merge(ed_user)
