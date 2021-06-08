import asyncio
from concurrent.futures import ThreadPoolExecutor
from game import game

startGame = True
Game = game()

clients = []
thread_pool = ThreadPoolExecutor()

def start_game():
    for client in clients:
        client.transport.write(("Zaczynamy " + "\r\n").encode())

class HostServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.loop = asyncio.get_running_loop()
        print("Initiate server")

    def play(self):
        print("zaczynamy gre")

    def connect_client(self):
        print("Poloaczono klienta")
        for client in clients:
            client.transport.write(("Dołączył " + self.name + "\r\n").encode())
        Game.numberOfPlayers += 1

    def connection_made(self, transport) -> None:
        self.transport = transport
        self.addr = transport.get_extra_info("peername")
        print("Connection from " + str(self.addr))
        self.name = None
        clients.append(self)

    def data_received(self, data: bytes) -> None:
        message = data.decode()
        if "CONNECT" in message:
            self.name = message.split("CONNECT ")[1].split("\r\n")[0]
            if startGame:
                asyncio.create_task(self.async_connect_client())

        if "ANSWERS" in message:
            nick = message.split("CONNECT ")[1].split("\r\n")[0]

    async def async_connect_client(self):
        task = await self.loop.run_in_executor(thread_pool, self.connect_client)

    async def async_game(self):
        task = await self.loop.run_in_executor(thread_pool, self.play)

# loop = asyncio.get_event_loop()
# coroutine = loop.create_server(HostServerProtocol, server_host, server_port)
# server = loop.run_until_complete(coroutine)
#
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass
#
# server.close()
# loop.run_until_complete(server.wait_closed())
# loop.close()
