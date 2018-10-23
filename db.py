"""
Create DB
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, \
                        ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref

engine = create_engine('sqlite:///project_files/db.db?check_same_thread=False')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Clients(Base):
    # таблица с клиентамии
    __tablename__ = 'clients'
    id = Column(Integer(), primary_key=True, index=True)
    phone = Column(String(50), index=True, unique=True)
    name = Column(String(50))
    full_name = Column(String(255))
    city = Column(String(50))
    full_address = Column(String(255))
    company = Column(String(50))


class Sent(Base):
    # отправленные смс
    __tablename__ = 'sent'
    id = Column(Integer(), primary_key=True)
    phone = Column(String(50), ForeignKey('clients.phone'), index=True)
    sms_id = Column(String(50), index=True)
    mes = Column(String(200))
    date = Column(DateTime)
    client = relationship(Clients, backref=backref('sent', uselist=False))


class Received(Base):
    # полученные смс
    __tablename__ = 'received'
    id = Column(Integer(), primary_key=True)
    sms_id = Column(String(50), index=True)
    phone = Column(String(50), ForeignKey('clients.phone'), index=True)
    mes = Column(Text, index=True)
    sent = Column(DateTime)  # conv to time?
    time = Column(DateTime)  # conv to time?
    client = relationship(Clients, backref=backref('received'))


class Bills(Base):
    # выставленные счета
    __tablename__ = 'bills'
    id = Column(Integer(), primary_key=True)
    client_id = Column(Integer(), ForeignKey('clients.id'), index=True)
    bill_num = Column(Integer())
    file_path = Column(Text)
    client = relationship(Clients, backref=backref('bills'))


'''
class Status(Base):
    # статус клиента
    __tablename__ = 'status'
    id = Column(Integer(), primary_key=True)
    client_id = Column(Integer(), ForeignKey('clients.id'))
    status = Column(String(25), default='New')

'''
if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)




