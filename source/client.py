import socket
from playerData import PlayerData
from GUI import GUIApp

DATA_SIZE = 12
player_data = PlayerData()
round_num = 0


def receive(s):
    data = b""
    while b"\r\n" not in data:
        data += s.recv(DATA_SIZE)
    return data.decode().split('\r\n')[0]


def client_gameplay(host):
    global app, round_num
    host = host.split(' ')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host[0], int(host[1])))
    server.sendall(("CONNECT " + player_data.nick + "\r\n").encode())
    try:
        while True:
            data = receive(server)
            if "OK" in data:
                host_name = data.split("OK ")[1]
                print("Dołączyłeś do pokoju gracza " + host_name + "! Przejdź do interfejsu gry!")
                app = GUIApp(host_name, player_data.nick)

            elif "NEW_PLAYER" in data:
                print("Gracz " + data.split("NEW_PLAYER ")[1].split("\r\n")[0] + " - dołączył do pokoju!")

            elif "ROUND_START" in data:
                while True:
                    if app.is_created():
                        break
                curr_letter = data.split("ROUND_START ")[1].split(" ")[0]
                round_time = data.split("ROUND_START ")[1].split(" ")[1] + " " + data.split("ROUND_START ")[1].split(" ")[2]
                print("\nLitera: " + curr_letter)
                app.start_game(curr_letter, round_time)

            elif "END_ROUND" in data:
                round_num += 1
                player_data.categories = app.get_values()
                app.set_letter("-")
                print("Koniec rundy " + str(round_num) + "!")
                app.set_warning("Koniec rundy!", "green")
                server.sendall(("ANSWERS " + player_data.answers_to_pickle() + "\r\n").encode())

            elif "RESULTS" in data:
                results = data.split("RESULTS ")[1].split("\r\n")[0]
                print("Wynik: ")
                player_data.show_answers_and_save_score(results)
                app.set_score(player_data.score)
                app.set_warning("Oczekiwanie na hosta!", "blue")
                print("Oczekiwanie na rozpoczęcie kolejnej rundy przez hosta!")

            elif "END_GAME" in data:
                print("Host opuścił pokój! Do zobaczenia następnym razem!")
                server.close()
                app.callback()
                return
            else:
                print(data)
    except socket.error:
        print("Host opuścił pokój! Do zobaczenia następnym razem!")
        server.close()
        app.callback()
        return
