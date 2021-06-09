import socket
import asyncio
import random
import string
import time
import _thread
from host import *
from game import Game
from concurrent.futures import ThreadPoolExecutor

hash_room=""
game = Game()
clients = []
thread_pool = ThreadPoolExecutor()


def notify_clients(message):
    for client in clients:
        client.transport.write((message + "\r\n").encode())

def receiving_answers(answers):
    game.addAnswers(answers)


def host_loop(s):
    global game
    game = Game()
    game.answers.nick = input("Podaj swój nick:\n")

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
    while True:
        curr_letter = random.choice(string.ascii_letters)
        game.character = curr_letter
        notify_clients("ROUND_START " + curr_letter)

        _thread.start_new_thread(game.writeAnswer, ())
        time.sleep(40)
        game.time_end = True
        game.addAnswers(game.answersToPickle())
        notify_clients("END_ROUND")
        time.sleep(10)
        game.calculateResults()
        game.showScoreAndAnswers()
        msg = game.scoreBoardtoPickle()
        notify_clients("RESULTS " + msg)


        i=input("Czy chcesz zaczac kolejna runde? 0=NIE 1=TAK")
        if i == '0':
            break
        elif i == '1':
            game.time_end = False
            game.scoreboard.clear()
            print("Zaczynam kolejna runde")


class HostServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.loop = asyncio.get_running_loop()
        print("Initiate server")

    def connection_made(self, transport) -> None:
        self.transport = transport
        self.addr = transport.get_extra_info("peername")
        print("Connection from " + str(self.addr))
        self.name = None

    def data_received(self, data: bytes) -> None:
        message = data.decode()
        if "CONNECT" in message:
            self.name = message.split("CONNECT ")[1].split("\r\n")[0]
            asyncio.create_task(self.async_connect_client())
        elif "ANSWERS" in message:
            answers = message.split("ANSWERS ")[1].split("\r\n")[0]
            asyncio.create_task(self.async_receiving_answers(answers))

    async def async_connect_client(self):
        await self.loop.run_in_executor(thread_pool, notify_clients, "NEW_PLAYER " + self.name)
        print("Połączono klienta. Nazwa gracza: " + self.name + " Adres gracza: " + str(self.addr))
        game.numberOfPlayers += 1
        clients.append(self)
        self.transport.write("200 OK\r\n".encode())


    async def async_receiving_answers(self, answers):
        await self.loop.run_in_executor(thread_pool, receiving_answers, answers)
