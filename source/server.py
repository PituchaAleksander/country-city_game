import asyncio
import hashlib
from concurrent.futures import ThreadPoolExecutor

server_host = "127.0.0.1"
server_port = 80
room_info = {}


# metoda tworzenia pokoju gry
def create_room(address):
    room_password = hashlib.shake_256(str.encode("utf-8")).hexdigest(6)
    while room_password in room_info:
        room_password = hashlib.shake_256(str.encode("utf-8")).hexdigest(6)

    room_info[room_password] = address
    return room_password


def join():
    pass


def game_start():
    pass


class CountryCityServerProtocol(asyncio.Protocol):
    def connection_made(self, transport) -> None:
        self.transport = transport
        self.addr = transport.get_extra_info("peername")
        print("Connection from " + str(self.addr))

    def data_received(self, data: bytes) -> None:
        message = data.decode()
        print("Data received: " + str(message))
        if "CREATE_ROOM" in message:
            asyncio.create_task(self.async_create_room())
        elif "JOIN" in message:
            pass
        elif "GAME_START" in message:
            pass

    async def async_create_room(self):
        task = await loop.run_in_executor(thread_pool, create_room)
        response = str(task).encode()
        print("Data sent: " + str(response))

        self.transport.write(response + "\r\n".encode())
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
