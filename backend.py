import random
from os import environ
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
import asyncio
from autobahn.wamp.types import SubscribeOptions
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

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
    customer_id = Column(Integer, ForeignKey("customers.id"))



class Component(ApplicationSession):

    async def onJoin(self, details):
        counter = 0
        while True:
            print(Customer)
            self.publish(Customer)

            obj = {'counter': counter, 'foo': [1, 2, 3]}
            print("publish: com.myapp.topic2")
            self.publish('com.myapp.topic2', random.randint(0, 100), 23, c="Hello", d=obj)

            counter += 1
            await asyncio.sleep(1)


if __name__ == '__main__':
    url = environ.get("AUTOBAHN_DEMO_ROUTER", "ws://127.0.0.1:8080/ws")
    realm = "realm1"
    runner = ApplicationRunner(url, realm)
    runner.run(Component)