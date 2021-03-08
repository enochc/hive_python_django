import asyncio
import time
from sav import channels
import toml


class Hive:

    def __init__(self, server, port, timeout=0, name="Python"):
        self.port = port
        self.server = server
        self.prop_receiver, self.prop_sender = channels.create()
        self.is_running = False
        self.reader, self.writer = None, None
        self.timeout = timeout
        self.properties = {}  # (name, value, type) tuple
        self.name = name
        self.peers = []  # list of strings
        self.peer_message = ""
        self.changed = False

    # def properties(self):
    #     return self.prop_receiver

    def stop(self):
        if self.writer is not None:
            self.writer.close()
        self.is_running = False

    async def wait(self):
        if self.timeout > 0:
            await asyncio.sleep(self.timeout)
            print(f"done")
            self.stop()

    async def run(self):
        print(f"connect hive client to {self.server} {self.port}")
        self.reader, self.writer = await asyncio.open_connection(self.server, self.port)
        print(f">>>>>>> {self.writer}")
        self.is_running = True
        await asyncio.gather(
            self.receive(),
            self.listen(self.reader),
            self.wait(),
        )

        self.writer.close()
        await self.writer.wait_closed()

    async def listen(self, reader):
        async with channels.open(self.prop_sender):

            # send header after connect:
            header = b'\x72'
            header_name = b'\x78'
            peer_request = b'\x65'
            properties = b'\x10'
            property = b'\x11'
            delete = b'\x12'
            peer_message = b'\x13'

            eol = bytes("\n", 'utf-8')
            ba = "HVEP".encode()+eol+header_name+self.name.encode()+eol

            print(f".... send: {ba}")
            # await self.write(ba)
            self.writer.write(ba)
            # request peers
            await self.write(peer_request)
            while self.is_running and not reader.at_eof():
                try:
                    size_bytes = await reader.read(4)
                    size = int.from_bytes(size_bytes, 'big')
                    print(f"size: {size}")
                    msg = await reader.read(size)
                    msg_type = msg[0].to_bytes(1, 'big', signed=False)
                    msg = msg[1:].decode()
                    print(f"received: {msg_type}, {msg}")
                    # new properties
                    if msg_type == properties:
                        t_data = toml.loads(msg)
                        print(f"Received properties: {msg}")
                        for prop in t_data:
                            data = t_data[prop]
                            # name, value, type
                            # await self.prop_sender.asend((prop, data, data.__class__.__name__))
                            self.properties[prop] = data
                    # received single propery
                    elif msg_type == property:
                        print(f"Received property: {msg}")
                        t_data = toml.loads(msg)
                        for prop in t_data:
                            data = t_data[prop]
                            self.update_property(prop, data,  data.__class__.__name__)
                    elif msg_type == delete:
                        for p in self.properties:
                            if p[0] == msg:
                                self.properties.remove(p)
                                self.changed = True
                    elif msg_type == peer_request:  # Peers list
                        print(f"got peers: {msg}")
                        self.peers.clear()
                        for p in msg.split(","):
                            s = p.split("|")[0]
                            print(f"{s}")
                            self.peers.append(s)
                            self.changed = True
                    elif msg_type == peer_message:  # Peer message
                        self.peer_message = msg
                        self.changed = True

                except Exception as e:
                    print(f"closing...{e}")
                    break

    async def send_to_peer(self, peer_name, msg):
        msg = f"|s|{peer_name}|=|{msg}"
        await self.write(msg)

    async def write(self, p_bytes):
        len_bytes = len(p_bytes).to_bytes(4, 'big', signed=False)
        self.writer.write(len_bytes)
        self.writer.write(p_bytes)
        print(f"write {p_bytes}")
        await self.writer.drain()
        print("written")

    def update_property(self, name, value, type):
        if type == "str":
            self.properties[name] = str(value)
        elif type == bool:
            self.properties[name] = bool(value)
        else:  #integer
            self.properties[name] = int(value)

    def set_prop(self, name, value, type):
        print(f"Save Value: {name} = {value}")
        b = b'\x11'
        if type == "str":
            msg = b+ f"{name}='{value}'".encode()
        elif type == "bool":
            val = format(f"{value}").lower()
            msg = b+ f"{name}={val}".encode()
        else:
            msg = b+f"{name}={value}".encode()

        self.update_property(name, value, type)
        asyncio.run(self.write(msg))

    async def receive(self):
        async for prop in self.prop_receiver:
            # self.properties.append(prop)
            # self.properties[prop[0]] = prop[1]
            self.changed = True
            print(f"received prop: {prop}")


# hive = Hive("127.0.0.1", 3000, timeout=3)
#
# stuff = asyncio.run(hive.run())
#
# print(f"stuff: {stuff}")
