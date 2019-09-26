from datetime import datetime

# from sqlalchemy.dialects.mysql import
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    String,
    VARCHAR
)
from sqlalchemy import func
from sqlalchemy.orm import relationship
from .meta import Base


# class MyModel(Base):
#     __tablename__ = 'models'
#     id = Column(Integer, primary_key=True)
#     name = Column(Text)
#     value = Column(Integer)
#
# Index('my_index', MyModel.name, unique=True, mysql_length=255)
#

class _Request(Base):
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True)
    create_date=Column(DateTime, default=func.current_timestamp())
    name=Column(VARCHAR(255))
    answers = relationship("Answer",backref='answer', cascade='none')
    count=Column(Integer)
    def __init__(self,request):
        self.name=request.GET['query']
        self.create_date=func.current_timestamp()
        self.request=request
        self.count=0
    def add_request(self):
        self.request.dbsession.add(self)
        # req=request.dbsession.query(self).filter(self.name == request.GET['query']).first()
        # return req.id




# Index('request_index', _Request.name, unique=True, mysql_length=255)

class Answer(Base):
    __tablename__ = 'answer'
    # id = Column(Integer, primary_key=True)
    link = Column(VARCHAR(255))
    title=Column(VARCHAR(255))
    tags=Column(VARCHAR(255))
    question_id=Column(VARCHAR(60), primary_key=True)
    creation_date=Column(DateTime)
    last_activity_date=Column(DateTime)
    request_id = Column(Integer, ForeignKey('request.id'))

    # request = relationship("_Request", backref='answers')
    def __init__(self,answer):
        self.link = answer['link']
        self.title = answer['title']
        self.creation_date = datetime.fromtimestamp(int(answer['creation_date']))
        self.last_activity_date = datetime.fromtimestamp(int(answer['last_activity_date']))
        self.question_id = answer['question_id']
        self.request_id=None


    def update_answers(self,id,dbsession):
        self.request_id = id
        dbsession.merge(self)

    def add_answers(self,id,request):
        self.request_id=id
        request.dbsession.add(self)









# Index('request_index',Answer.title, unique=True, mysql_length=500)


