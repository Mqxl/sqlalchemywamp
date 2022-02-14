import sys
from autobahn.asyncio import ApplicationSession
from database import *
from jsonencoder import *

sys.setrecursionlimit(99999)


class Component(ApplicationSession):

    async def onJoin(self, details):

        async def post_customer(id, uuid, name, email):

            Database.session.add(Database.insert(id=id, uuid=uuid, name=name, email=email))
            Database.session.commit()

            return 'success'

        async def post_meter(id, uuid, name, description, customer_id):
            Database.session.add(Database.meter(id=id, uuid=uuid, name=name, description=description, customer_id=customer_id))
            Database.session.commit()
            return 'success'

        async def update_customer(customerid, id, uuid, name, email):
            Database.update_cust(customerid=customerid, id=id, uuid=uuid, name=name, email=email)

            Database.session.commit()
            return 'success'

        async def update_meter(customerid, id, uuid, name, description, customer_id):
            Database.update_meter(
                customerid=customerid, id=id, uuid=uuid, name=name, description=description, customer_id=customer_id)
            Database.session.commit()

            return 'success'

        async def detail_customer(id):
            return json.dumps(Database.detail_customer(id=id), cls=AlchemyEncoder)

        async def delete_customer(id):
            Database.delete_customer(id)
            Database.session.commit()
            return 'Deleted'

        async def delete_meter(id):
            Database.delete_meter(id)
            Database.session.commit()
            return 'Deleted'

        async def detail_meter(id):
            return json.dumps(Database.detail_meter(id=id), cls=AlchemyEncoder)

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
