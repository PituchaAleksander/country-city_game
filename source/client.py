import socket
import threading
from game import *

DATA_SIZE = 12
client_game = Game()


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
    server.sendall(("CONNECT " + client_game.answers.nick + "\r\n").encode())
    t = threading.Thread(target=client_game.writeAnswer, args=())
    while True:
        data = receive(server)
        print("Data received: " + data)
        if "OK" in data:
            print("Dołączyłeś do pokoju gracza " + data.split("OK ")[1] + "!")
        elif "NEW_PLAYER" in data:
            print("Gracz " + data.split("NEW_PLAYER ")[1].split("\r\n")[0] + " - dołączył do pokoju!")
        elif "ROUND_START" in data:
            print("ROUND START!!!")
            # if t.is_alive():
            #     t.join()
            #     t = threading.Thread(target=game.writeAnswer, args=())
            curr_letter = data.split("ROUND_START ")[1].split("\r\n")[0]
            client_game.character = curr_letter
            client_game.time_end = False
            t.start()
        elif "END_ROUND" in data:
            client_game.time_end = True
            print("\nKoniec rundy! Wyjdź z udzielania odpowiedzi!")
            server.sendall(("ANSWERS " + client_game.answersToPickle() + "\r\n").encode())
            if t.is_alive():
                print("ZARAZ BEDE Czekal")
                t.join()

            t = threading.Thread(target=client_game.writeAnswer, args=())
            print("JUZ POCZEKALEM")
        elif "RESULTS" in data:
            results = data.split("RESULTS ")[1].split("\r\n")[0]
            client_game.pickleToScoreBoard(results)
            client_game.showScoreAndAnswers()
        elif "END_GAME" in data:
            server.close()
            break
        else:
            print(data)
