import socket
import asyncio
import _thread
from game import Game
from concurrent.futures import ThreadPoolExecutor
from game import Game
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
            print("Connected to host game!")
        elif "RESULTS" in data:
            results = data.split("RESULTS ")[1].split("\r\n")[0]
            global game
            game.jsonToScoreBoard(results)
            game.showScoreAndAnswers()
        else:
            print(data)