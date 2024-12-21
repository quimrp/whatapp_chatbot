from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Float, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    window_quotes = relationship("WindowQuote", back_populates="user")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wamid = Column(String, unique=True, index=True)
    sender_id = Column(String, index=True)
    content = Column(JSON)
    message_type = Column(String)
    timestamp = Column(DateTime, server_default=func.now())

    multimedia_message = relationship("MultimediaMessage", back_populates="message", uselist=False)
    order = relationship("Order", back_populates="message", uselist=False)

class MultimediaMessage(Base):
    __tablename__ = "multimedia_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey('messages.id'), unique=True)
    media_type = Column(String)
    media_id = Column(String)
    media_url = Column(String)

    message = relationship("Message", back_populates="multimedia_message")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey('messages.id'), unique=True)
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

    order = relationship("Order", back_populates="items")

class FlowState(Base):
    __tablename__ = "flow_states"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True, index=True)
    current_flow = Column(String, nullable=False, default="none")
    current_node = Column(String, nullable=True)
    context = Column(JSON, nullable=True)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

class WindowQuote(Base):
    __tablename__ = "window_quotes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=False)
    status = Column(String, nullable=False)

    user = relationship("User", back_populates="window_quotes")
    windows = relationship("Window", back_populates="quote")

class Window(Base):
    __tablename__ = "windows"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quote_id = Column(Integer, ForeignKey('window_quotes.id'), nullable=False)
    reference = Column(String)
    width = Column(Float)
    height = Column(Float)
    color = Column(String)
    has_blind = Column(Boolean)
    motorized_blind = Column(Boolean)
    opening_type = Column(String)
    image_url = Column(String)

    quote = relationship("WindowQuote", back_populates="windows")

