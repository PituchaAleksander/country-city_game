import socket
from client import client_gameplay, player_data
from host import host_loop, host_player_data, game_data

server_host = "127.0.0.1"
server_port = 80

DATA_SIZE = 12


def receive(s):
    data = b""
    while b"\r\n" not in data:
        data += s.recv(DATA_SIZE)
    return data.decode().split('\r\n')[0]


def start_app():
    host_player_data.nick = player_data.nick = input("Podaj swój nick: ")
    while True:
        i = input("---------------\nMenu:\n[1] Stwórz gre\n[2] Dołącz do gry\nPodaj numer: ")

        if i == '1':  # =========Host=========
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect((server_host, server_port))

            server.sendall("CREATE_ROOM\r\n".encode())
            data = receive(server)
            if "201" in data:
                game_data.password = data.split("CREATED ")[1]
                print("Teraz możesz zaprosić innych graczy do gry! Hasło pokoju: {}".format(game_data.password))
                return host_loop(server.getsockname())
            else:
                print(data)
        elif i == '2':  # =========Client=========
            token = input("Podaj hasło pokoju: ")

            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect((server_host, server_port))

            server.sendall("JOIN {}\r\n".format(token).encode())
            data = receive(server)
            if "202" in data:
                return client_gameplay(data.split("EXISTS ")[1])
            else:
                print(data)


start_app()
