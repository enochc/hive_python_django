
import threading
import asyncio

from .hive import Hive


class DHive:
    def __init__(self, name):
        # self.hive = Hive("127.0.0.1", 3000, name=name)
        self.hive = Hive("192.168.5.48", 3000, name=name)
        # 192.168.5.48
        t = threading.Thread(target=self.do_run)
        t.setDaemon(True)
        t.start()

    def changed(self):
        if self.hive.changed:
            self.hive.changed = False
            return True
        else:
            return False

    def properties(self):
        return self.hive.properties

    def peers(self):
        return filter(lambda x: x != self.hive.name, self.hive.peers)

    def name(self):
        return self.hive.name

    def do_run(self):
        asyncio.run(self.hive.run())

    def send_to_peer(self, peer_name, msg):
        asyncio.run(self.hive.send_to_peer(peer_name, msg))

    def save(self, name, value, type):
        self.hive.set_prop(name, value, type)

    def peer_message(self):
        return self.hive.peer_message
