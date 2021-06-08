import socket
import asyncio
import _thread
from game import Game
from concurrent.futures import ThreadPoolExecutor
from host import *
from client import *

DATA_SIZE = 12

def receive(s):
    data = b""
    while b"\r\n" not in data:
        data += s.recv(DATA_SIZE)
    return data.decode().split('\r\n')[0]

def start_app():
    while True:
        i = input("Co chcesz zrobić:\n"
                  "[1] Stwórz gre\n"
                  "[2] Dołącz do gry\n")
        if i == '1':
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect(("localhost", 80))

            server.sendall("CREATE_ROOM\r\n".encode())
            data = receive(server)
            if "201" in data:
                global hash_room
                hash_room = data.split("CREATED ")[1]
                print("Podaj to hasło innym: {}".format(hash_room))
                host_loop(server.getsockname())
                break
            else:
                print(data)
        elif i == '2':
            token = input("Podaj token:")

            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect(("localhost", 80))
            server.sendall("JOIN {}\r\n".format(token).encode())

            data = receive(server)
            if "202" in data:
                print(data)
                client_game(data.split("EXISTS ")[1])

                break
            else:
                print(data)


start_app()