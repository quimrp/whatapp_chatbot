from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True)
    waba_id = Column(String)
    phone_number_id = Column(String)
    from_number = Column(String)
    to = Column(String)
    pushname = Column(String)
    type = Column(String)
    body = Column(String)
    time = Column(String)
    raw_data = Column(String)

class MediaMessage(Base):
    __tablename__ = "media_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String, ForeignKey('messages.id'))
    media_id = Column(String)
    link = Column(String)

class QuotedMessage(Base):
    __tablename__ = "quoted_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String, ForeignKey('messages.id'))
    quoted_data = Column(String)

