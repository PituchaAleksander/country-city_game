import socket
import asyncio
import _thread
from source.host import *

hash_room = ""

def receive(s):
    data = b""
    while not b"\r\n" in data:
        data += s.recv(DATA_SIZE)
    return data.decode().split('\r\n')[0]

def game_loop(s):
    _thread.start_new_thread(client_host_input, ())
    loop = asyncio.get_event_loop()
    coroutine = loop.create_server(HostServerProtocol, s[0], s[1])
    server = loop.run_until_complete(coroutine)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

def client_host_input():
    i = input("Podaj cos aby przerwac")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("localhost", 80))
    print(hash_room)
    server.sendall("GAME_START {}\r\n".format(hash_room).encode())
    start_game()


def connect_with_host(s):
    data = s.split(' ')
    print(data)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((data[0], int(data[1])))
    server.sendall("CONNECT dupa\r\n".encode())
    while True:
        print(receive(server))


def start_app():
    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect(("localhost", 80))
        print(server.getsockname())

        i = input("Co chcesz zrobić:\n"
                  "[1] Stwórz gre\n"
                  "[2] Dołącz do gry")
        if i == '1':
            server.sendall("CREATE_ROOM\r\n".encode())
            data = receive(server)
            if "201" in data:
                global hash_room
                hash_room = data.split("CREATED ")[1]
                print("Podaj to hasło innym: {}".format(hash_room))
                game_loop(server.getsockname())
                break
            else:
                print(data)
        elif i == '2':
            token = input("Podaj token:")
            server.sendall("JOIN {}\r\n".format(token).encode())
            data = receive(server)
            if "202" in data:
                print(data)
                connect_with_host(data.split("EXISTS ")[1])

                break
            else:
                print(data)


DATA_SIZE = 12
print(start_app())
