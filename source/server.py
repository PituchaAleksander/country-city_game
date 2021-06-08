import asyncio
import random
from concurrent.futures import ThreadPoolExecutor

server_host = "127.0.0.1"
server_port = 80
room_info = {}


# metoda tworzenia pokoju gry
def create_room(address):
    room_password = hex(random.getrandbits(24))[2:]
    while room_password in room_info:
        room_password = hex(random.getrandbits(24))[2:]

    room_info[room_password] = address
    return room_password


# metoda dołączania do istniejącego pokoju
def join_room(password):
    if password in room_info:
        return room_info[password]
    else:
        return None


def game_start():
    pass


class CountryCityServerProtocol(asyncio.Protocol):
    def connection_made(self, transport) -> None:
        self.transport = transport
        self.addr = transport.get_extra_info("peername")
        print("Connection from " + str(self.addr))

    def data_received(self, data: bytes) -> None:
        message = data.decode()
        print("Data received: " + str(message.split("\r\n")[0]))
        if "CREATE_ROOM" in message:
            asyncio.create_task(self.async_create_room())
        elif "JOIN" in message:
            room_pass = message.split("\r\n")[0]
            asyncio.create_task(self.async_join_room(int(room_pass)))
        elif "GAME_START" in message:
            pass

    async def async_create_room(self):
        task = await loop.run_in_executor(thread_pool, create_room, self.addr)
        response = str(task).encode()
        print("Data sent: " + str(response))

        self.transport.write("201 CREATED ".encode() + response + "\r\n".encode())
        self.transport.close()

    async def async_join_room(self, password):
        task = await loop.run_in_executor(thread_pool, join_room, password)
        if task:
            response = str(task).encode()
            print("Data sent: " + str(response))

            self.transport.write("200 EXISTS ".encode() + response + "\r\n".encode())
            self.transport.close()
        else:
            print("Room doesn't exists! Sent NOT_EXISTS.")
            self.transport.write("404 NOT_EXISTS\r\n".encode())
            self.transport.close()


thread_pool = ThreadPoolExecutor()

loop = asyncio.get_event_loop()
coroutine = loop.create_server(CountryCityServerProtocol, server_host, server_port)
server = loop.run_until_complete(coroutine)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
