import socket
import threading
from game import *

DATA_SIZE = 12

game = Game()

def receive(s):
    data = b""
    while b"\r\n" not in data:
        data += s.recv(DATA_SIZE)
    return data.decode().split('\r\n')[0]


def client_game(host):
    global game
    game = Game()
    game.answers.nick = input("Podaj swój nick:\n")

    host = host.split(' ')
    print(host)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host[0], int(host[1])))
    server.sendall(("CONNECT "+game.answers.nick+"\r\n").encode())
    t = threading.Thread(target=game.writeAnswer, args=())
    while True:
        data = receive(server)
        print("od seerwa" + data)
        if "OK" in data:
            print("Connected to host game! Wait for the host to start the game.")
        elif "NEW_PLAYER" in data:
            print("Gracz " + data.split("NEW_PLAYER ")[1].split("\r\n")[0] + " - dołączył do gry")
        elif "ROUND_START" in data:
            print("ROUND START!!!")
            # if t.is_alive():
            #     t.join()
            #     t = threading.Thread(target=game.writeAnswer, args=())
            curr_letter = data.split("ROUND_START ")[1].split("\r\n")[0]
            game.character = curr_letter
            game.time_end = False
            t.start()
        elif "END_ROUND" in data:
            game.time_end = True
            print("\nKoniec rundy! Wyjdź z udzielania odpowiedzi!")
            server.sendall(("ANSWERS "+game.answersToPickle()+"\r\n").encode())
            if t.is_alive():
                print("ZARAZ BEDE Czekal")
                t.join()

            t = threading.Thread(target=game.writeAnswer, args=())
            print("JUZ POCZEKALEM")
        elif "RESULTS" in data:
            results = data.split("RESULTS ")[1].split("\r\n")[0]
            game.pickleToScoreBoard(results)
            game.showScoreAndAnswers()
        elif "END_GAME" in data:
            server.close()
            break
        else:
            print(data)
