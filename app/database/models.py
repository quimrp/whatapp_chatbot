from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wamid = Column(String, unique=True, index=True)
    waba_id = Column(String)
    phone_number_id = Column(String)
    from_number = Column(String)
    to = Column(String)
    pushname = Column(String)
    type = Column(String)
    body = Column(String)
    time = Column(DateTime)
    raw_data = Column(String)

    interactive_message = relationship("InteractiveMessage", back_populates="message", uselist=False)
    multimedia_message = relationship("Multimediamessage", back_populates="message", uselist=False)
    order = relationship("Order", back_populates="message", uselist=False)

class InteractiveMessage(Base):
    __tablename__ = "interactive_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey('messages.id'))
    interactive_type = Column(String)
    content = Column(String)

    message = relationship("Message", back_populates="interactive_message")

class Multimediamessage(Base):
    __tablename__ = "multimedia_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey('messages.id'))
    media_type = Column(String)
    media_id = Column(String)
    media_url = Column(String)

    message = relationship("Message", back_populates="multimedia_message")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey('messages.id'))
    catalog_id = Column(String)
    status = Column(Enum('recibido', 'preparacion', 'enviado', 'entregado', name='order_status'))
    total_price = Column(Float)
    order_time = Column(DateTime, server_default=func.now())

    message = relationship("Message", back_populates="order")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_retailer_id = Column(String)
    catalog_id = Column(String)
    item_id = Column(String)
    quantity = Column(Integer)
    item_price = Column(Float)
    currency = Column(String)
    item_order = Column(Integer)

    order = relationship("Order", back_populates="items")

