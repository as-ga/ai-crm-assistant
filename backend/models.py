from typing import List
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
import datetime


class TimestampMixin:
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)


class Customer(Base, TimestampMixin):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(20))
    company: Mapped[str] = mapped_column(String(100))

    # Relationships
    conversations: Mapped[List["Conversation"]
                          ] = relationship(back_populates="customer")
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="customer")
    orders: Mapped[List["Order"]] = relationship(back_populates="customer")


class Conversation(Base, TimestampMixin):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.id"))
    title: Mapped[str] = mapped_column(String(255))

    # Relationships
    customer: Mapped["Customer"] = relationship(back_populates="conversations")
    messages: Mapped[List["Message"]] = relationship(
        back_populates="conversation")


class Message(Base, TimestampMixin):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    conversation_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("conversations.id"))
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(String)

    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages")


class Ticket(Base, TimestampMixin):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.id"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String(50))
    priority: Mapped[str] = mapped_column(String(20))

    # Relationships
    customer: Mapped["Customer"] = relationship(back_populates="tickets")


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.id"))
    amount: Mapped[float] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(50))

    # Relationships
    customer: Mapped["Customer"] = relationship(back_populates="orders")
