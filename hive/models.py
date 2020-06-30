
import threading
import asyncio

from .hive import Hive


class DHive:
    def __init__(self, thing):
        self.thing = thing
        self.hive = Hive("127.0.0.1", 3000)

        t = threading.Thread(target=self.do_run)
        t.setDaemon(True)
        t.start()

    def properties(self):
        return self.hive.properties

    def do_run(self):
        asyncio.run(self.hive.run())

    def save(self, name, value, type):
        self.hive.set_prop(name, value, type)
