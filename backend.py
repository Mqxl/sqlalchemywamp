import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import Column, Integer, String, ForeignKey
from os import environ
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from sqlalchemy.orm import sessionmaker


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





class Component(ApplicationSession):

    async def onJoin(self, details):
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
                return Database.session.query(Customer).get(id)

            def delete_customer(id):
                return Database.session.query(Customer).filter(Customer.id == id).delete()

            def delete_meter(id):
                return Database.session.query(MeterType).filter(MeterType.id == id).all()

            def detail_meter(id):
                return Database.session.query(MeterType).get(id)

            def find_meter(id):
                return Database.session.query(MeterType).filter(MeterType.customer_id == id).all()

        class AlchemyEncoder(json.JSONEncoder):

            async def default(self, obj):
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

        async def post_customer(id, uuid, name, email):

            Database.session.add(Database.insert(id=id, uuid=uuid, name=name, email=email))
            Database.session.commit()

            return 'success'

        async def post_meter(id, uuid, name, description, customer_id):
            Database.session.add(Database.meter(id=id, uuid=uuid, name=name, description=description, customer_id=customer_id))
            Database.session.commit()
            return 'success'

        async def update_customer(customerid, id, uuid, name, email):
            await Database.update_cust(customerid=customerid, id=id, uuid=uuid, name=name, email=email)

            Database.session.commit()
            return 'success'

        async def update_meter(customerid, id, uuid, name, description, customer_id):
            await Database.update_meter(
                customerid=customerid, id=id, uuid=uuid, name=name, description=description, customer_id=customer_id)
            Database.session.commit()

            return 'success'

        async def detail_customer(id):
            return json.dumps(Database.detail_customer(id=id), cls=AlchemyEncoder)

        async def delete_customer(id):
            await Database.delete_customer(id)
            Database.session.commit()
            return 'Deleted'

        async def delete_meter(id):
            await Database.delete_meter(id)
            Database.session.commit()
            return 'Deleted'

        async def detail_meter(id):
            return json.dumps(Database.detail_meter(id), cls=AlchemyEncoder)

        async def find_meter(id):
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
