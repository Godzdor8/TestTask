from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Message(Base):
    __tablename__ = 'messages'
    id = Column(String, primary_key=True)
    number = Column(String)
    type = Column(String)
    publish_date = Column(DateTime)
    finish_reason = Column(String)

    debtor_id = Column(Integer, ForeignKey('debtors.id'))
    debtor = relationship("Debtor", back_populates="messages")

    banks = relationship("Bank", back_populates="message")
    obligations = relationship("MonetaryObligation", back_populates="message")
    payments = relationship("ObligatoryPayment", back_populates="message")

class Debtor(Base):
    __tablename__ = 'debtors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_date = Column(DateTime)
    birth_place = Column(String)
    address_index = Column(String)
    region = Column(String)
    city = Column(String)
    street = Column(String)
    house = Column(String)
    flat = Column(String)
    inn = Column(String)

    messages = relationship("Message", back_populates="debtor")

class Bank(Base):
    __tablename__ = 'banks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    bik = Column(String)

    message_id = Column(String, ForeignKey('messages.id'))
    message = relationship("Message", back_populates="banks")

class MonetaryObligation(Base):
    __tablename__ = 'monetary_obligations'
    id = Column(Integer, primary_key=True)
    creditor_name = Column(String)
    content = Column(String)
    basis = Column(String)
    total_sum = Column(Float)
    debt_sum = Column(Float)
    penalty_sum = Column(Float)

    message_id = Column(String, ForeignKey('messages.id'))
    message = relationship("Message", back_populates="obligations")

class ObligatoryPayment(Base):
    __tablename__ = 'obligatory_payments'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sum = Column(Float)

    message_id = Column(String, ForeignKey('messages.id'))
    message = relationship("Message", back_populates="payments")