import socket
import asyncio
import random
import string
import time
import threading
from game import Game
from concurrent.futures import ThreadPoolExecutor
from GUI import App

server_host = "127.0.0.1"
server_port = 80

host_game = Game()
clients = []
thread_pool = ThreadPoolExecutor()


def notify_clients(message):
    for client in clients:
        client.transport.write((message + "\r\n").encode())


def receiving_answers(answers):
    host_game.addAnswers(answers)


def host_loop(s):
    threading.Thread(target=host_gameplay, args=()).start()
    loop = asyncio.get_event_loop()
    coroutine = loop.create_server(HostServerProtocol, s[0], s[1])
    server = loop.run_until_complete(coroutine)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


def host_gameplay():
    start_command = input("Napisz \"START\", aby rozpocząć!\n")
    while "START" not in start_command.upper():
        start_command = input("Napisz \"START\", aby rozpocząć!\n")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((server_host, server_port))
    server.sendall("GAME_START {}\r\n".format(host_game.password).encode())
    while True:
        curr_letter = random.choice(string.ascii_letters)
        host_game.character = curr_letter
        notify_clients("ROUND_START " + curr_letter)

        app = App()

        time.sleep(20)
        host_game.answers = app.get_values()
        app.callback()
        host_game.addAnswers(host_game.answersToPickle())
        notify_clients("END_ROUND")
        time.sleep(2)
        host_game.calculateResults()
        host_game.showScoreAndAnswers()
        msg = host_game.scoreBoardtoPickle()
        notify_clients("RESULTS " + msg)

        i = input("Czy chcesz zaczac kolejna runde? 0=NIE 1=TAK")
        if i == '0':
            break
        elif i == '1':
            host_game.time_end = False
            host_game.scoreboard.clear()
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
        host_game.numberOfPlayers += 1
        print("Gracz " + self.name + " dołączył! Liczba graczy w pokoju: " + str(host_game.numberOfPlayers + 1) + "\nNapisz \"START\", aby rozpocząć!")
        clients.append(self)
        self.transport.write(("200 OK " + host_game.answers.nick + "\r\n").encode())

    async def async_receiving_answers(self, answers):
        await self.loop.run_in_executor(thread_pool, receiving_answers, answers)
