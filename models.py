"""

ORM is used for convenience.

Database usage:
 - db_connect: validate settings
 - create_table: in case first time open
 - get session: see insert_item(),
    ref -> http://docs.sqlalchemy.org/en/rel_1_0/orm/session.html
 - use this session to add and commit new sql_item

"""

from sqlalchemy import create_engine, Column, String, \
    Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import relationship, backref
import settings

from sqlalchemy.ext.declarative import declarative_base
DeclarativeBase = declarative_base()


def db_connect():
    """
    Validate database settings and
    :return: a METHOD to create session, usage(after get return):
      session = Session()

    """
    # TODO: need to check/increase available pool size?
    engine = create_engine(URL(**settings.DATABASE))

    try:
        engine.connect()
        engine.dispose()
    except (OperationalError, ):
        raise ValueError("Check database settings!")

    return engine

def create_tables(engine):
    """
    Initialize database, WON'T break existing data.
    This actions take some time(about 0.015~0.02s), so make it happen once,
    only when start crawling.
    """
    DeclarativeBase.metadata.create_all(engine)

def insert_item(session, sql_item):
    """
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()

    :param session:
    :param sql_item: Issue or Article
    :return:
    """
    try:
        session.add(sql_item)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

class Issue(DeclarativeBase):

    __tablename__ = 'issue'

    # Example: http://weekly.caixin.com/2015/cw658/index.html
    # 豪门与“山寨”之盟 <- Cover story
    # 2015年6月29日出版 <- publish_date
    # 总期号：660 <- id

    id = Column(Integer, primary_key=True)
    publish_date = Column(DateTime)
    cover_story = Column(String)
    url = Column(String)

    # TODO: make sure this works, for example we have either instance
    # - issue = someIssue()
    # - issue.articles.all()

    # - article = someArticle()
    # - article.relate_issue.articles.all()

    # ref: http://stackoverflow.com/questions/7420670/how-do-i-access-the-related-foreignkey-object-from-a-object-in-sqlalchemy
    # ref: http://docs.sqlalchemy.org/en/rel_1_0/orm/relationships.html
    articles = relationship('Article', backref='issue')

    def next_issue(self):
        pass

    def previous_issue(self):
        pass


class Article(DeclarativeBase):

    __tablename__ = 'article'

    # Example:
    # http://weekly.caixin.com/[2015-01-02]/[100770279].html

    # TODO: add `issue_id-` as prefix to make sure uniqueness
    id = Column(Integer, primary_key=True)
    url = Column(String)

    abstract = Column(String, nullable=True)
    author = Column(String, nullable=True)
    content = Column(String)

    # TODO: convenient 1-to-many query for both
    # articles under same issue and publish date
    relate_issue = Column(Integer, ForeignKey('issue.id'))


def test():

    engine = db_connect()
    create_tables(engine)
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=rr)
    session = Session()
    aaa = Issue(id=1, publish_date='20150101',
                title='java: the best programming language.')
    session.add(aaa)
    session.commit()
    # import ipdb; ipdb.set_trace()
    bbb = Article(id='2', url='123', content='123', relate_issue=1)
    session.add(bbb)
    session.commit()
    session.query(Article)

