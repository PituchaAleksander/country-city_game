import socket
import asyncio
import random
import string
import time
import threading
import datetime
from gameData import GameData
from playerData import PlayerData
from concurrent.futures import ThreadPoolExecutor
from GUI import App

server_host = "127.0.0.1"
server_port = 80

game_data = GameData()
host_player_data = PlayerData()
clients = []
thread_pool = ThreadPoolExecutor()


def notify_clients(message):
    for client in clients:
        client.transport.write((message + "\r\n").encode())

#==================Uruchomienie serwera zdarzeniowego hosta==================
def host_loop(s):
    threading.Thread(target=host_gameplay, args=()).start()
    loop = asyncio.get_event_loop()
    coroutine = loop.create_server(HostServerProtocol, s[0], s[1])
    loop.run_until_complete(coroutine)
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
    server.sendall("GAME_START {}\r\n".format(game_data.password).encode())
    while True:
# ==================Ustawienie/wysłanie litery==================
        curr_letter = random.choice(string.ascii_letters)
        game_data.character = curr_letter
        app = App(host_player_data.nick)
                    # TU WYWALA APKE BO INNY WATEK BUDUJE APP A SET_TIME JEST SZYBSZE I CHCE USTAWIC NULL
        round_time = (datetime.datetime.now() + datetime.timedelta(seconds=20)).strftime("%Y-%m-%d %H:%M:%S")
        notify_clients("ROUND_START " + curr_letter + " " + round_time)
        app.set_time(round_time)

        print("Litera: " + curr_letter)

# ==================Start wpisywania==================
        time.sleep(20)
        host_player_data.categories = app.get_values()
        app.callback()
        game_data.addAnswers(host_player_data.answersToPickle())

# ==================Zakończenie rundy==================
        notify_clients("END_ROUND")
        time.sleep(2)

# ==================Liczenie wyników==================
        game_data.calculateResults()
        host_player_data.showScoreAndAnswers(game_data.scoreBoardtoPickle())

# ==================Wysyłanie wyników do graczy==================
        msg = game_data.scoreBoardtoPickle()
        notify_clients("RESULTS " + msg)

# ==================Koniec/Nowa runda==================
        i = input("Czy chcesz zaczac kolejna runde? 0=NIE 1=TAK")
        if i == '0':
            break
        elif i == '1':
            game_data.time_end = False
            game_data.scoreboard.clear()
            print("Zaczynam kolejna runde")

# ====================================HostServerProtocol====================================

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
        game_data.numberOfPlayers += 1
        print("Gracz " + self.name + " dołączył! Liczba graczy w pokoju: " + str(game_data.numberOfPlayers + 1) + "\nNapisz \"START\", aby rozpocząć!")
        clients.append(self)
        self.transport.write(("200 OK " + host_player_data.nick + "\r\n").encode())

    async def async_receiving_answers(self, answers):
        await self.loop.run_in_executor(thread_pool, game_data.addAnswers, answers)
