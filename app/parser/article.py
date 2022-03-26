from sqlalchemy import Column, String, Integer, Date, Float

from base import Base


class Article(Base):
    __tablename__ = 'news'

    id = Column(String, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    release_time = Column(Float)
    link = Column(String)
    description = Column(String)


    def __init__(self, id, title, release_date, release_time, link, description):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.release_time = release_time
        self.link = link
        self.description = description