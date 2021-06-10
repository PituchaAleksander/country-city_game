import socket
import threading
import time

from playerData import *
from GUI import App

DATA_SIZE = 12
player_data = PlayerData()


def receive(s):
    data = b""
    while b"\r\n" not in data:
        data += s.recv(DATA_SIZE)
    return data.decode().split('\r\n')[0]


def client_gameplay(host):
    host = host.split(' ')
    print(host)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host[0], int(host[1])))
    server.sendall(("CONNECT " + player_data.nick + "\r\n").encode())
    while True:
        data = receive(server)
        if "OK" in data:
            print("Dołączyłeś do pokoju gracza " + data.split("OK ")[1] + "!")
            app = App(player_data.nick)

        elif "NEW_PLAYER" in data:
            print("Gracz " + data.split("NEW_PLAYER ")[1].split("\r\n")[0] + " - dołączył do pokoju!")

        elif "ROUND_START" in data:
            print("ROUND START!!!")
            curr_letter = data.split("ROUND_START ")[1].split(" ")[0]
            round_time = data.split("ROUND_START ")[1].split(" ")[1] + " " + data.split("ROUND_START ")[1].split(" ")[2]
            print("Litera: " + curr_letter + "Round start: " + round_time)
            app.set_letter(curr_letter)
            app.set_time(round_time)

        elif "END_ROUND" in data:
            player_data.categories = app.get_values()
            app.set_letter("-")
            print("\nKoniec rundy! Wyjdź z udzielania odpowiedzi!")
            server.sendall(("ANSWERS " + player_data.answersToPickle() + "\r\n").encode())

        elif "RESULTS" in data:
            results = data.split("RESULTS ")[1].split("\r\n")[0]
            player_data.showScoreAndAnswers(results)
            app.set_score(player_data.score)

        elif "END_GAME" in data:
            server.close()
            app.callback()
            break
        else:
            print(data)
