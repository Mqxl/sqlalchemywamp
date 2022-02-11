import random
from os import environ

import asyncio
from autobahn.wamp.types import SubscribeOptions
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    An application component that subscribes and receives events of no
    payload and of complex payload, and stops after 5 seconds.
    """

    async def onJoin(self, details):
        self.received = 0

        def on_heartbeat(details=None):
            print("Got heartbeat (publication ID {})".format(details.publication))

        await self.subscribe(on_heartbeat, 'com.myapp.heartbeat', options=SubscribeOptions(details_arg='details'))

        def on_topic2(a, b, c=None, d=None):
            print("Got event: {} {} {} {}".format(a, b, c, d))

        await self.subscribe(on_topic2, 'com.myapp.topic2')
        asyncio.get_event_loop().call_later(5, self.leave)

    def onDisconnect(self):
        asyncio.get_event_loop().stop()


if __name__ == '__main__':
    url = environ.get("AUTOBAHN_DEMO_ROUTER", "ws://127.0.0.1:8080/ws")
    realm = "realm1"
    runner = ApplicationRunner(url, realm)
    runner.run(Component)