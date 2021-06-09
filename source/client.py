import socket
import _thread
from game import *
# from app import

DATA_SIZE = 12
game = Game()


def receive(s):
    data = b""
    while b"\r\n" not in data:
        data += s.recv(DATA_SIZE)
    return data.decode().split('\r\n')[0]


def client_game(host):
    host = host.split(' ')
    print(host)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host[0], int(host[1])))
    server.sendall("CONNECT dupa\r\n".encode())
    while True:
        data = receive(server)
        if "OK" in data:
            print("Connected to host game! Wait for the host to start the game.")
        elif "ROUND_START" in data:
            write = True
            _thread.start_new_thread(game.writeAnswer, ())
        elif "END_ROUND" in data:
            write = False
        elif "RESULTS" in data:
            results = data.split("RESULTS ")[1].split("\r\n")[0]
            global game
            game.jsonToScoreBoard(results)
            game.showScoreAndAnswers()
        elif "END_GAME" in data:
            server.close()
            break
        else:
            print(data)
