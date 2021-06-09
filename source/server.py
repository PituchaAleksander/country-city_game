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


# metoda gdy gra się rozpocznie
def game_start(password):
    if password in room_info:
        room_info.pop(password)
        return True
    else:
        return False


class CountryCityServerProtocol(asyncio.Protocol):
    def connection_made(self, transport) -> None:
        self.transport = transport
        self.addr = transport.get_extra_info("peername")
        print("[Server] Connection from " + str(self.addr))

    def data_received(self, data: bytes) -> None:
        message = data.decode()
        print("[Client " + str(self.addr[0]) + " - " + str(self.addr[1]) + "] Data received: " + str(message.split("\r\n")[0]))
        if "CREATE_ROOM" in message:
            asyncio.create_task(self.async_create_room())
        elif "JOIN" in message:
            room_pass = message.split("JOIN ")[1].split("\r\n")[0]
            asyncio.create_task(self.async_join_room(room_pass))
        elif "GAME_START" in message:
            room_pass = message.split("GAME_START ")[1].split("\r\n")[0]
            asyncio.create_task(self.async_game_start(room_pass))

    async def async_create_room(self):
        task = await loop.run_in_executor(thread_pool, create_room, self.addr)
        response = str(task).encode()
        print("[Client " + str(self.addr[0]) + " - " + str(self.addr[1]) + "] Data sent: 201 CREATED " + str(response.decode()))

        self.transport.write("201 CREATED ".encode() + response + "\r\n".encode())
        self.transport.close()

    async def async_join_room(self, password):
        task = await loop.run_in_executor(thread_pool, join_room, password)
        if task:
            response = str(task[0]) + ' ' + str(task[1])
            print("[Client " + str(self.addr[0]) + " - " + str(self.addr[1]) + "] Data sent: 202 EXISTS " + str(response))

            self.transport.write("202 EXISTS ".encode() + response.encode() + "\r\n".encode())
            self.transport.close()
        else:
            print("[Client " + str(self.addr[0]) + " - " + str(self.addr[1]) + "] Data sent: 404 NOT_EXISTS")
            self.transport.write("404 NOT_EXISTS\r\n".encode())
            self.transport.close()

    async def async_game_start(self, password):
        task = await loop.run_in_executor(thread_pool, game_start, password)
        if task:
            print("[Client " + str(self.addr[0]) + " - " + str(self.addr[1]) + "] Data sent: 200 OK")
            self.transport.write("200 OK\r\n".encode())
            self.transport.close()
        else:
            print("[Client " + str(self.addr[0]) + " - " + str(self.addr[1]) + "] Data sent: 404 ERROR")
            self.transport.write("404 ERROR\r\n".encode())
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
