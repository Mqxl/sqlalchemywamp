import asyncio
import sys
from jsonencoder import *
from os import environ
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
import pprint
import requests

class Component(ApplicationSession):

    async def onJoin(self, details):
        check = input()
        if check == 'post customer':
            print('Write id:')
            id = input()
            print('Write uuid:')
            uuid = input()
            print('Write name:')
            name = input()
            print('Write email:')
            email = input()
            starred = await self.call('com.arguments.post_customer', id, uuid, name, email)
            print("Post complete: {}".format(starred))
            self.leave()
        elif check == 'post meter':
            print('Write id:')
            id = input()
            print('Write uuid:')
            uuid = input()
            print('Write name:')
            name = input()
            print('Write description:')
            description = input()
            print('Write customer id:')
            customer_id = input()
            starred = await self.call('com.arguments.post_meter', id, uuid, name, description, customer_id)
            print("Post complete: {}".format(starred))
            self.leave()
        elif check == 'update meter':
            print('Write update meter:')
            customerid = input()
            print('Write id:')
            id = input()
            print('Write uuid:')
            uuid = input()
            print('Write name:')
            name = input()
            print('Write description:')
            description = input()
            print('Write customer_id:')
            customer_id = input()
            starred = await self.call('com.arguments.update_meter', customerid, id, uuid, name, description,
                                      customer_id)
            print("Post complete: {}".format(starred))
            self.leave()
        elif check == 'update customer':
            print('Write update customer:')
            customerid = input()
            print('Write id:')
            id = input()
            print('Write uuid:')
            uuid = input()
            print('Write name:')
            name = input()
            print('Write email:')
            email = input()
            starred = await self.call('com.arguments.update_customer', customerid, id, uuid, name, email)
            print("Post complete: {}".format(starred))
            self.leave()
        elif check == 'delete customer':
            print('customer id')
            id = input()
            starred = await self.call('com.arguments.delete_customer', id)
            print("Deleted: {}".format(starred))
            self.leave()

        elif check == 'delete meter':
            print('meter id')
            id = input()
            starred = await self.call('com.arguments.delete_meter', id)
            print("Deleted: {}".format(starred))
            self.leave()

        elif check == 'detail customer':
            print('Write id:')
            id = input()
            starred = await self.call('com.arguments.detail_customer', id)
            print("Customer name: {}".format(starred))
            self.leave()

        elif check == 'detail meter':
            print('Write id:')
            id = input()
            starred = await self.call('com.arguments.detail_meter', id)
            print("Meter name: {}".format(starred))
            self.leave()

        elif check == 'find meter':
            print('Write customer id:')
            id = input()
            starred = await self.call('com.arguments.find_meter', id)
            print("Meter: {}".format(starred))
            self.leave()

    def onDisconnect(self):
        asyncio.get_event_loop().stop()


if __name__ == '__main__':
    url = environ.get("AUTOBAHN_DEMO_ROUTER", "ws://127.0.0.1:8080/ws")
    realm = "realm1"
    runner = ApplicationRunner(url, realm)
    runner.run(Component)
