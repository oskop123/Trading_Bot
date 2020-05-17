## Zadanie 1
### 1.1
Pliki do zadania 1 znajdują się w folderze Zad1. Poszerz działanie programu o przechowywanie aktualnego stanu konta - *portfolio*.
Kroki postępowania:
- w pliku *data_storage.py* zmodyfikuj metodę *fetch_data()* klasy *DataStorage* tak, aby pobierała dane o stanie konta z API. Polecenie, które należy przekazać do serwera to *getMarginLevel* (bez dodatkowych argumentów). Serwer odpowie następującą strukturą:\
{ <br>
    "status": true,\
    "returnData": { <br>
    "balance": 995800269.43,\
    "credit": 1000.00,\
    "currency": "PLN",\
    "equity": 995985397.56,\
    "margin": 572634.43,\
    "margin_free": 995227635.00,\
    "margin_level": 173930.41\
    } <br>	
} <br>
<!-- End of list -->
Przykład komunikacji z API znajduje się np. w metodzie *sell()* klasy *DataStorage*
- zapisz pole *equity* znajdujące się w części *returnData* do zmiennej *money*.
- zmienną *money* przekaż do metody *update_portfolio()* (metodę tę utworzymy w następnym punkcie) obiektu *s*, który reprezentuje jedną z obserwowanych spółek
- w pliku *MovingAverageCrossoverStrategy.py*, w klasie *Macs* zainicjalizuj w konstruktorze listę *portfolio*, która będzie przechowywała zmieniającą się wartość stanu konta
- dopisz do klasy *Macs* metodę *update_portfolio()*, która przyjmuje argument *money* i dopisuje go do listy *portfolio*\
Na tym etapie program powinien zapisywać na bieżąco wszystkie zmieny stanu konta.
### 1.2
Czas poszerzyć metodę *raport* klasy *Macs* o możliwość raportowania stanu konta:
- dodaj do DataFramu *df* kolumnę *Poftfolio* i pszechowaj w niej zmienną *portfolio*
- do *fig* dodaj subplot, który narysuje wykres zmian w portfolio.
