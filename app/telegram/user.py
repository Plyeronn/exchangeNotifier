from sqlalchemy import Column, String, Integer, Float

from base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    time_created = Column(Float)
    status = Column(String)
    last_seen = Column(Float)

    def __init__(self, id, time_created, status):
        self.id = id
        self.time_created = time_created
        self.status = status
        self.last_seen = 0