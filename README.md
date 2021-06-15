# Gra sieciowa ***Państwa-Miasta***

Aplikacja sieciowa w języku Python wykorzystująca niskopoziomowy interfejs sieciowy - socket.  
Gra polega na podawaniu słów z różnych dziedzin rozpoczynających się na zadaną literę.

## Twórcy
<table>
  <tr>
    <td align="center"> <a href="https://github.com/PituchaAleksander"><img src="https://avatars.githubusercontent.com/u/63605795?v=4" width="100px;" alt=""/><br><sub><b>Aleksander Pitucha</b></sub></a></td>
    <td align="center"> <a href="https://github.com/PrzemyslawSalek"><img src="https://avatars.githubusercontent.com/u/66259490?v=4" width="100px;" alt=""/><br><sub><b>Przemysław Sałek</b></sub></a></td>
    <td align="center"> <a href="https://github.com/szymix1999"><img src="https://avatars.githubusercontent.com/u/66270215?v=4" width="100px;" alt=""/><br><sub><b>Szymon Sala</b></sub></a></td>
  </tr>
</table>

## Wymagania
  * Python 3.7 +
  * Moduły: socket, asyncio, pickle, tkinter, ThreadPoolExecutor (concurrent.futures)

## Użycie:
1. Uruchomienie serwera
```bash
python server.py
```
2. Uruchomienie klienta
```bash
python app.py
```
Następnie należy postępować zgodnie z poleceniami wyświetlanymi w konsoli oraz interfejsie graficznym klienta.

## Przebieg gry:
1. Wylosowanie litery przez system gry.
2. Od momentu wylosowania litery wszyscy gracze zaczynają wpisywać słowa zaczynające się na wylosowaną literę – po jednym słowie pasującym do danej kategorii. Wpisywane wyrazy nie powinny być wyrażeniami zbyt ogólnymi. Między innymi błędem jest użycie słowa dinozaur w kategorii zwierzęta. Wpisywanie słów kończy się, gdy skończy się czas przeznaczony na rundę.
3. Zliczanie punktów – wszyscy gracze otrzymują po jednym punkcie za każde poprawne słowo z danej kategorii.
4. Gra toczy się tak długo, jak tylko gracze mają na to ochotę.

## Dokumentacja:
- <a href="https://github.com/PituchaAleksander/country-city_game/blob/main/docs/Dokument%20projektowy.pdf">Dokument projektowy</a>
### Inne dokumenty:
- <a href="https://github.com/PituchaAleksander/country-city_game/blob/main/docs/Schemat%20blokowy%20aplikacji.png">Schemat blokowy aplikacji</a>
- <a href="https://github.com/PituchaAleksander/country-city_game/blob/main/docs/Struktura%20sieci.png">Struktura sieci</a>
- <a href="https://github.com/PituchaAleksander/country-city_game/blob/main/docs/Diagram%20komunikacji%20serwer-klient.png">Diagram komunikacji serwer-klient</a>
- <a href="https://github.com/PituchaAleksander/country-city_game/blob/main/docs/Diagram%20komunikacji%20host-klient.png">Diagram komunikacji host-klient</a>
