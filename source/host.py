import asyncio
import socket
import _thread
from host import *
from concurrent.futures import ThreadPoolExecutor
from game import Game

game = Game()
hash_room=""

clients = []
thread_pool = ThreadPoolExecutor()

def sendClientStart():
    for client in clients:
        client.transport.write(("Zaczynamy " + "\r\n").encode())

def host_loop(s):
    _thread.start_new_thread(host_game, ())
    loop = asyncio.get_event_loop()
    coroutine = loop.create_server(HostServerProtocol, s[0], s[1])
    server = loop.run_until_complete(coroutine)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


def host_game():
    input("Podaj cos aby zaczac gre")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("localhost", 80))
    server.sendall("GAME_START {}\r\n".format(hash_room).encode())
    sendClientStart()
    while True:
        json_string = game.writeAnswer("a")
        game.addAnswers(json_string)


        i=input("Czy chcesz zaczac kolejna runde? 0=NIE 1=TAK")
        if i == '0':
            break
        elif i == '1':
            print("Zaczynam kolejna runde")

class HostServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.loop = asyncio.get_running_loop()
        print("Initiate server")

    def play(self, answers):
        print("zaczynamy gre")

    def connect_client(self):
        print("Połączono klienta. Nazwa gracza: " + self.name + " Adres gracza: " + str(self.addr))
        for client in clients:
            client.transport.write(("Dołączył " + self.name + "\r\n").encode())
        game.numberOfPlayers += 1

        self.transport.write("200 OK\r\n".encode())

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
            asyncio.create_task(self.async_connect_client())

        if "ANSWERS" in message:
            answers = message.split("ANSWERS ")[1].split("\r\n")[0]
            asyncio.create_task(self.async_game(answers))

    async def async_connect_client(self):
        await self.loop.run_in_executor(thread_pool, self.connect_client)

    async def async_game(self, answers):
        await self.loop.run_in_executor(thread_pool, self.play, answers)
