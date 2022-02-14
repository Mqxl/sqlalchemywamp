import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import Column, Integer, String, ForeignKey
from os import environ
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from sqlalchemy.orm import sessionmaker
from jsonencoder import *


class Postgre(object):
    def connect(self):
        db_string = "postgresql+psycopg2://postgres:postgres@0.0.0.0/postgres"
        db = create_engine(db_string)
        return db


Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String)
    name = Column(String, unique=True)
    email = Column(String, unique=True)


class MeterType(Base):
    __tablename__ = "meter-types"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String)
    name = Column(String)
    description = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE", onupdate='CASCADE'))


class Database(object):
    con = Postgre()
    Session = sessionmaker(con.connect())
    session = Session()
    Base.metadata.create_all(con.connect())

    def insert(id, uuid, name, email):
        return Customer(id=id, uuid=uuid, name=name, email=email)

    def meter(id, uuid, name, description, customer_id):
        return MeterType(id=id, uuid=uuid, name=name, description=description, customer_id=customer_id)

    def update_cust(id, uuid, name, email, customerid):
        return Database.session.query(Customer).filter(Customer.id == customerid).update(
            {"id": id, "uuid": uuid, "name": name, "email": email})

    def update_meter(id, uuid, name, description, customerid, customer_id):
        return Database.session.query(MeterType).filter(MeterType.id == customerid).update(
            {"id": id, "uuid": uuid, "name": name, "description": description, "customer_id": customer_id})

    def detail_customer(id):
        get = Database.session.query(Customer).get(id).name
        return get

    def delete_customer(id):
        return Database.session.query(Customer).filter(Customer.id == id).delete()

    def delete_meter(id):
        return Database.session.query(MeterType).filter(MeterType.id == id).delete()

    def detail_meter(id):
        get = Database.session.query(MeterType).get(id).name
        return get

    def find_meter(id):
        get = Database.session.query(MeterType).filter(MeterType.customer_id == id)
        return get
