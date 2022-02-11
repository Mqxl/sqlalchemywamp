import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import Column, Integer, String, ForeignKey
from os import environ
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from sqlalchemy.orm import sessionmaker
db_string = "postgresql+psycopg2://postgres:postgres@0.0.0.0/postgres"

db = create_engine(db_string)
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


Session = sessionmaker(db)
session = Session()
Base.metadata.create_all(db)


class Component(ApplicationSession):

    async def onJoin(self, details):
        class Database(object):
            def insert(id, uuid, name, email):
                return Customer(id=id, uuid=uuid, name=name, email=email)

            def meter(id, uuid, name, description, customer_id):
                return MeterType(id=id, uuid=uuid, name=name, description=description, customer_id=customer_id)

            def update_cust(id, uuid, name, email, customerid):
                return session.query(Customer).filter(Customer.id == customerid).update({"id": id, "uuid": uuid, "name": name, "email": email})

            def update_meter(id, uuid, name, description, customerid, customer_id):
                return session.query(MeterType).filter(MeterType.id == customerid).update({"id": id, "uuid": uuid, "name": name, "description": description, "customer_id": customer_id})

            def detail_customer(id):
                return session.query(Customer).get(id)

            def delete_customer(id):
                return session.query(Customer).filter(Customer.id == id).delete()

            def delete_meter(id):
                return session.query(MeterType).filter(MeterType.id == id).all()

            def detail_meter(id):
                return session.query(MeterType).get(id)

            def find_meter(id):
                return session.query(MeterType).filter(MeterType.customer_id == id).all()

        class AlchemyEncoder(json.JSONEncoder):

            def default(self, obj):
                if isinstance(obj.__class__, DeclarativeMeta):

                    fields = {}
                    for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                        data = obj.__getattribute__(field)
                        try:
                            json.dumps(data)
                            fields[field] = data
                        except TypeError:
                            fields[field] = None

                    return fields

                return json.JSONEncoder.default(self, obj)

        def post_customer(id, uuid, name, email):

            session.add(Database.insert(id=id, uuid=uuid, name=name, email=email))
            session.commit()

            return 'success'

        def post_meter(id, uuid, name, description, customer_id):
            session.add(Database.meter(id=id, uuid=uuid, name=name, description=description, customer_id=customer_id))
            session.commit()
            return 'success'

        def update_customer(customerid ,id, uuid, name, email):
            Database.update_cust(customerid=customerid, id=id, uuid=uuid, name=name, email=email)

            session.commit()
            return 'success'

        def update_meter(customerid ,id, uuid, name, description, customer_id):
            Database.update_meter(customerid=customerid, id=id, uuid=uuid, name=name, description=description, customer_id=customer_id)
            session.commit()

            return 'success'

        def detail_customer(id):
            return json.dumps(Database.detail_customer(id=id), cls=AlchemyEncoder)

        def delete_customer(id):
            Database.delete_customer(id)
            session.commit()
            return 'Deleted'

        def delete_meter(id):
            Database.delete_meter(id)
            session.commit()
            return 'Deleted'

        def detail_meter(id):
            return json.dumps(Database.detail_meter(id), cls=AlchemyEncoder)

        def find_meter(id):
            return json.dumps(Database.find_meter(id), cls=AlchemyEncoder)

        await self.register(post_customer, 'com.arguments.post_customer')
        await self.register(post_meter, 'com.arguments.post_meter')
        await self.register(update_customer, 'com.arguments.update_customer')
        await self.register(update_meter, 'com.arguments.update_meter')
        await self.register(detail_customer, 'com.arguments.detail_customer')
        await self.register(detail_meter, 'com.arguments.detail_meter')
        await self.register(find_meter, 'com.arguments.find_meter')
        await self.register(delete_customer, 'com.arguments.delete_customer')
        await self.register(delete_meter, 'com.arguments.delete_meter')
        print("Registered methods; ready for frontend.")


if __name__ == '__main__':
    url = environ.get("AUTOBAHN_DEMO_ROUTER", "ws://127.0.0.1:8080/ws")
    realm = "realm1"
    runner = ApplicationRunner(url, realm)
    runner.run(Component)
