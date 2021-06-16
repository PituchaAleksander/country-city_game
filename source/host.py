import socket
import asyncio
import random
import string
import time
import threading
import datetime
import os
import uuid
from gameData import GameData
from playerData import PlayerData
from concurrent.futures import ThreadPoolExecutor
from GUI import GUIApp

server_host = "127.0.0.1"
server_port = 80

game_data = GameData()
host_player_data = PlayerData()
clients = []
responses_from_client = {}
thread_pool = ThreadPoolExecutor()
round_num = 0


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
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
        print("Do zobaczenia!")
        os._exit(0)


def host_gameplay():
    global round_num
    start_command = input("Napisz \"START\", aby rozpocząć!\n")
    while "START" not in start_command.upper():
        start_command = input("Napisz \"START\", aby rozpocząć!\n")
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((server_host, server_port))
        server.sendall("GAME_START {}\r\n".format(game_data.password).encode())
    except socket.error:
        print("Błąd! Serwer nie odpowiada!")
        notify_clients("END_GAME")
        os._exit(0)
        return

    # ==================Zamykanie pokoju==================
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((server_host, server_port))
    server.sendall("GAME_START {}\r\n".format(game_data.password).encode())

    # ==================Oczekiwanie na uruchomienie GUI==================
    app = GUIApp(host_player_data.nick, host_player_data.nick)
    while True:
        if app.is_created():
            break
    # ==================Główna pętla gry==================
    while True:
        # ================== Ustawienie/wysłanie litery ==================
        game_data.set_letter(random.choice(string.ascii_letters))
        print("Przełącz się na interfejs gry. Runda zaraz się rozpocznie!")
        time.sleep(5)
        print("\nLitera: " + game_data.letter)
        round_time = (datetime.datetime.now() + datetime.timedelta(seconds=(game_data.round_time + 1))).strftime("%Y-%m-%d %H:%M:%S")
        notify_clients("ROUND_START " + game_data.letter + " " + round_time)
        responses_from_client.clear()
        app.start_game(game_data.letter, round_time)

        # ================== Start wpisywania ==================
        time.sleep(game_data.round_time)
        host_player_data.categories = app.get_values()
        game_data.add_answers(host_player_data.answers_to_pickle(), host_player_data.nick)

        # ================== Zakończenie rundy ==================
        app.set_letter("-")
        app.set_warning("Oczekiwanie na odpowiedzi...", "blue")
        notify_clients("END_ROUND")

        #================== Oczekiwanie na odpowiedzi graczy ==================
        while len(clients) != len(responses_from_client):
            pass
        app.set_warning("Wróć do konsoli!", "blue")

        # ================== Liczenie wyników ==================
        game_data.calculate_results()
        round_num += 1
        print("Koniec rundy " + str(round_num) + "!\nWynik:")
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
                print("Do zobaczenia!")
                app.callback()
                notify_clients("END_GAME")
                os._exit(0)
                return


# ====================================HostServerProtocol====================================

class HostServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.loop = asyncio.get_running_loop()
        self.session_id = None

    def connection_made(self, transport) -> None:
        self.transport = transport
        self.addr = transport.get_extra_info("peername")
        # print("[SERVER-HOST]: Połączono " + str(self.addr))
        self.name = None

    def data_received(self, data: bytes) -> None:
        message = data.decode()
        if "CONNECT" in message:
            self.name = message.split("CONNECT ")[1].split("\r\n")[0]
            asyncio.create_task(self.async_connect_client())
        elif "ANSWERS" in message:
            asyncio.create_task(self.async_receiving_answers(message))

    def connection_lost(self, ex):
        print("[SERVER-HOST]: Rozłączono {}".format(self.name))
        clients.remove(self)

    def answer_service(self, message):
        if responses_from_client.get(self.session_id) is None:
            responses_from_client[self.session_id] = "ok"
            game_data.add_answers(message.split("ANSWERS ")[1].split("\r\n")[0], self.name)

    def check_client(self):
        exists = False
        for client in clients:
            if client.name == self.name:
                exists = True
                break

        if host_player_data.nick == self.name:
            exists = True

        if exists:
            clients.append(self)
            self.name = "duplikat " + self.name
            self.transport.write(("NOT_OK\r\n").encode())
        else:
            threading.Thread(target=notify_clients, args=("NEW_PLAYER " + self.name, )).start()
            print("[SERVER-HOST]: Gracz " + self.name + " dołączył! Liczba graczy w pokoju: " +
                  str(len(clients) + 1) + "\nNapisz \"START\", aby rozpocząć!")
            self.session_id = uuid.uuid4()
            clients.append(self)
            self.transport.write(("OK " + str(self.session_id) + " " + host_player_data.nick + "\r\n").encode())

    async def async_connect_client(self):
        await self.loop.run_in_executor(thread_pool, self.check_client)


    async def async_receiving_answers(self, message):
        if message.split(" ")[0] == str(self.session_id):
            await self.loop.run_in_executor(thread_pool, self.answer_service, message)
        else:
            self.transport.write("BAD_SESSION\r\n".encode())