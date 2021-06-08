import socket


def receive(s):
    data = b""
    while not b"\r\n" in data:
        data += s.recv(DATA_SIZE)
    return data.decode().split('\r\n')[0]


def start_app():
    while True:
        i = input("Co chcesz zrobić:\n"
                  "[1] Stwórz gre\n"
                  "[2] Dołącz do gry")
        if i == '2':
            token = input("Podaj token:")
            server.sendall("JOIN {}\r\n\r\n".format(token).encode())
        elif i == '1':
            server.sendall("CREATE_ROOM\r\n\r\n".encode())
        else:
            continue

        data = receive(server)
        if "201" in data:
            print("Podaj tego hasha innym: {}".format(data.split("CREATED")[1]))
            return "host"

        if "200" in data:
            print(data.split("200")[0])
            return "client"

        print(data)
        continue


DATA_SIZE = 12
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("localhost", 80))

print(start_app())
