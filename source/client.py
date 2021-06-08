import socket
import asyncio
from host import HostServerProtocol


def receive(s):
    data = b""
    while not b"\r\n" in data:
        data += s.recv(DATA_SIZE)
    return data.decode().split('\r\n')[0]

def game_loop(s):
    loop = asyncio.get_event_loop()
    coroutine = loop.create_server(HostServerProtocol, s[0], s[1])
    server = loop.run_until_complete(coroutine)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

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
            server.sendall("CREATE_ROOM\r\n\r\n".encode())
            data = receive(server)
            if "201" in data:
                print("Podaj tego hasha innym: {}".format(data.split("CREATED")[1]))
                game_loop(server.getsockname())
                break
            else:
                print(data)
        elif i == '2':
            token = input("Podaj token:")
            server.sendall("JOIN {}\r\n\r\n".format(token).encode())
            data = receive(server)
            if "202" in data:
                print(data)
                connect_with_host(data.split("EXISTS ")[1])

                break
            else:
                print(data)


DATA_SIZE = 12
print(start_app())
