import socket
from game import game


def receive(s):
    data = b""
    while not b"\r\n" in data:
        data += s.recv(DATA_SIZE)
    return data.decode().split('\r\n')[0]


def start_app():
    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect(("localhost", 80))

        i = input("Co chcesz zrobić:\n"
                  "[1] Stwórz gre\n"
                  "[2] Dołącz do gry")
        if i == '1':
            server.sendall("CREATE_ROOM\r\n\r\n".encode())
            data = receive(server)
            if "201" in data:
                print("Podaj tego hasha innym: {}".format(data.split("CREATED")[1]))
                #metoda dla gry host
                break
            else:
                print(data)
        elif i == '2':
            token = input("Podaj token:")
            server.sendall("JOIN {}\r\n\r\n".format(token).encode())
            if "202" in data:
                print(data.split("202")[0])
                #metoda dla gry klient
                break
            else:
                print(data)


DATA_SIZE = 12
print(start_app())
