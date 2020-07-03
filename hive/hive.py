import asyncio
import time
from sav import channels
import toml


class Hive:

    def __init__(self, server, port, timeout=0):
        self.port = port
        self.server = server
        self.prop_receiver, self.prop_sender = channels.create()
        self.is_running = False
        self.reader, self.writer = None, None
        self.timeout = timeout
        self.properties = []  # (name, value, type) tuple

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

        self.reader, self.writer = await asyncio.open_connection(
            self.server, self.port)
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
            while self.is_running and not reader.at_eof():
                try:
                    size_bytes = await reader.read(4)
                    size = int.from_bytes(size_bytes, 'big')
                    msg = await reader.read(size)
                    msg_type = msg[:3].decode()
                    msg = msg[3:].decode()
                    print(f"received: {msg_type}, {msg}")
                    # new property
                    if msg_type == "|P|":
                        t_data = toml.loads(msg)
                        for prop in t_data:
                            data = t_data[prop]
                            # name, value, type
                            await self.prop_sender.asend((prop, data, data.__class__.__name__))
                    elif msg_type == "|d|":
                        for p in self.properties:
                            if p[0] == msg:
                                self.properties.remove(p)

                except Exception as e:
                    print(f"closing...{e}")
                    break

    async def write(self, msg):
        len_bytes = len(msg).to_bytes(4, 'big', signed=False)
        self.writer.write(len_bytes)
        self.writer.write(msg.encode())
        print(f"write {msg}")
        await self.writer.drain()
        print("written")

    def set_prop(self, name, value, type):
        print(f"Save Value: {name} = {value}")

        if type == "str":
            msg = f"|p|{name}='{value}'"
        elif type == "bool":
            val = format(f"{value}").lower()
            msg = f"|p|{name}={val}"
        else:
            msg = f"|p|{name}={value}"

        asyncio.run(self.write(msg))

    async def receive(self):
        async for prop in self.prop_receiver:
            self.properties.append(prop)
            print(f"received prop: {prop}")


# hive = Hive("127.0.0.1", 3000, timeout=3)
#
# stuff = asyncio.run(hive.run())
#
# print(f"stuff: {stuff}")
