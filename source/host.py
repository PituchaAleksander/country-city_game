import socket
import asyncio
import random
import string
import time
import threading
import datetime
import os
from gameData import GameData
from playerData import PlayerData
from concurrent.futures import ThreadPoolExecutor
from GUI import GUIApp

server_host = "127.0.0.1"
server_port = 80

game_data = GameData()
host_player_data = PlayerData()
clients = []
thread_pool = ThreadPoolExecutor()


def notify_clients(message):
    for client in clients:
        client.transport.write((message + "\r\n").encode())


# ==================Uruchomienie serwera zdarzeniowego hosta==================
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
    server.sendall("GAME_START {}\r\n".format(game_data.password).encode())
    app = GUIApp(host_player_data.nick, host_player_data.nick)
    while True:
        if app.is_created():
            break
    while True:
        # ================== Ustawienie/wysłanie litery ==================
        game_data.set_letter(random.choice(string.ascii_letters))
        print("Przełącz się na interfejs gry. Runda zaraz się rozpocznie!")
        time.sleep(5)
        round_time = (datetime.datetime.now() + datetime.timedelta(seconds=21)).strftime("%Y-%m-%d %H:%M:%S")
        notify_clients("ROUND_START " + game_data.letter + " " + round_time)
        game_data.actual_response_number = 0
        app.start_game(game_data.letter, round_time)

        # ================== Start wpisywania ==================
        time.sleep(game_data.round_time)
        host_player_data.categories = app.get_values()
        game_data.add_answers(host_player_data.answers_to_pickle())

        # ================== Zakończenie rundy ==================
        app.set_letter("-")
        app.set_warning("Oczekiwanie na odpowiedzi", "blue")
        notify_clients("END_ROUND")

        #================== Oczekiwanie na odpowiedzi graczy ==================
        while len(clients) != game_data.actual_response_number:
            pass
        app.set_warning("Koniec rundy!", "green")

        # ================== Liczenie wyników ==================
        game_data.calculate_results()
        host_player_data.show_answers_and_save_score(game_data.score_board_to_pickle())
        app.set_score(host_player_data.score)

        # ================== Wysyłanie wyników do graczy ==================
        msg = game_data.score_board_to_pickle()
        notify_clients("RESULTS " + msg)

        # ================== Koniec/Nowa runda ==================
        while True:
            i = input("Czy chcesz zaczac kolejna runde?\n[1] TAK\n[2] NIE\n")
            if i == '1' or i.upper() == 'TAK':
                game_data.time_end = False
                game_data.scoreboard.clear()
                print("Kolejna runda się zaczęła! Wróć do interfejsu gry!")
                break
            elif i == '2' or i.upper() == 'NIE':
                app.callback()
                notify_clients("END_GAME")
                os._exit(0)
                return


# ====================================HostServerProtocol====================================

class HostServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.loop = asyncio.get_running_loop()

    def connection_made(self, transport) -> None:
        self.transport = transport
        self.addr = transport.get_extra_info("peername")
        # print("Connection from " + str(self.addr))
        self.name = None

    def data_received(self, data: bytes) -> None:
        message = data.decode()
        if "CONNECT" in message:
            self.name = message.split("CONNECT ")[1].split("\r\n")[0]
            asyncio.create_task(self.async_connect_client())
        elif "ANSWERS" in message:
            game_data.actual_response_number += 1
            answers = message.split("ANSWERS ")[1].split("\r\n")[0]
            asyncio.create_task(self.async_receiving_answers(answers))

    def connection_lost(self, ex):
        print("[SERVER-HOST]: Rozłączono {}".format(self.name))
        clients.remove(self)

    async def async_connect_client(self):
        await self.loop.run_in_executor(thread_pool, notify_clients, "NEW_PLAYER " + self.name)
        print("[SERVER-HOST]: Gracz " + self.name + " dołączył! Liczba graczy w pokoju: " +
              str(len(clients) + 1) + "\nNapisz \"START\", aby rozpocząć!")
        clients.append(self)
        self.transport.write(("200 OK " + host_player_data.nick + "\r\n").encode())

    async def async_receiving_answers(self, answers):
        await self.loop.run_in_executor(thread_pool, game_data.add_answers, answers)
