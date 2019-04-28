from contextlib import contextmanager

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, \
    Table, Text

engine = create_engine('sqlite:///:memory:')
Base = declarative_base()


post_keywords = Table('post_keywords', Base.metadata,
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('keyword_id', ForeignKey('keywords.id'), primary_key=True)
)


class BlogPost(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    headline = Column(String(255), nullable=False)
    body = Column(Text)

    # many to many BlogPost<->Keyword
    keywords = relationship('Keyword',
                            secondary=post_keywords,
                            back_populates='posts')

    def __init__(self, headline, body):
        self.headline = headline
        self.body = body

    def __repr__(self):
        return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.keywords)


class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)
    posts = relationship('BlogPost',
                         secondary=post_keywords,
                         back_populates='keywords')

    def __init__(self, keyword):
        self.keyword = keyword

    def __repr__(self):
        return "Keyword(%r)" % (self.keyword,)


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
    post = BlogPost("Wendy's Blog Post", "This is a test")
    session.add(post)

    post.keywords.append(Keyword('wendy'))
    post.keywords.append(Keyword('firstpost'))

    print(session.query(BlogPost)
          .filter(BlogPost.keywords.any(keyword='firstpost'))
          .all())

