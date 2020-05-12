# Trading Bot
Adam Księżyk i Oskar Świerczek

Aby rozpocząć działanie programu proszę uruchomić **Bot.py**.\
Uwaga! Interwał pobierania cen jest ustawiony na 1 min a długa średnia krocząca na 50 wartości, stąd prosty wniosek, że zanim program zacznie spekulację musi minąc co najmniej 50 min. Aby przyspieszyć proces można zmienić wartości zmiennych *long_window* i *interval*.

Plan działania programu:
- połączenie z API XTB
- przypisanie funkcji odbierającej wiadomości od API (*ticker_fun*)
- subskrybcja automatycznego wysyłania cen spółek przez API za pomocą sclienta
- odłączenie od API
- generowanie raportu

Plik **xAPIConnector.py** służy do kontroli API. Został pobrany ze strony XTB i zedytowany przez nas aby dpoasować go do projektu.

W pliku **data_storage.py** znajduje się klasa *DataStorage*. Jest to serce naszego projektu. Klasa ta jest odpowiedzialna za pobieranie i aktualizowanie danych oraz wysyłania ofert otwarcia i zamknięcia pozycji do API.

Strategia spekulacji, na której opiera się program zdefiniowana jest w klasie *Macs* w pliku **MovingAverageCrossoverStrategy.py**. Tam również przechowywane są dane każdgo instrumentu finansowego: cena, krótka i długa średnia krocząca oraz pozycje jakie chcemy zajmować.

Generowanie raportu końcowego z przebiegu całej spekulacji realizowane jest za pomocą funkcji raport. Obiekt klasy *DataStorage* zleca wykonanie raporu każdemu obiektowi klasy *Macs*.
Podsumowanie zawiera:
- wszystkie zapisane dane o instrumencie w formacie *.csv*
- wykres transakcji
