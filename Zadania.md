## Zadanie 1
### 1.1
Pliki do zadania 1 znajdują się w folderze Zad1. Poszerz działanie programu o przechowywanie aktualnego stanu konta - *portfolio*.
Kroki postępowania:
- w pliku *data_storage.py* zmodyfikuj metodę *fetch_data()* klasy *DataStorage* tak, aby pobierała dane o stanie konta z API. Polecenie, które należy przekazać do serwera to *getMarginLevel* (bez dodatkowych argumentów). Serwer odpowie następującą strukturą:\
{ <br>
&nbsp;&nbsp;&nbsp;&nbsp;"status": true,\
&nbsp;&nbsp;&nbsp;&nbsp;"returnData": { <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"balance": 995800269.43,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"credit": 1000.00,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"currency": "PLN",\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"equity": 995985397.56,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"margin": 572634.43,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"margin_free": 995227635.00,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"margin_level": 173930.41\
&nbsp;&nbsp;&nbsp;&nbsp;} <br>	
} <br>
Przykład komunikacji z API znajduje się np. w metodzie *sell()* klasy *DataStorage*
- zapisz pole *equity* znajdujące się w części *returnData* do zmiennej *money*.
- zmienną *money* przekaż do metody *update_portfolio()* (metodę tę utworzymy w następnym punkcie) obiektu *s*, który reprezentuje jedną z obserwowanych spółek
- w pliku *MovingAverageCrossoverStrategy.py*, w klasie *Macs* zainicjalizuj w konstruktorze listę *portfolio*, która będzie przechowywała zmieniającą się wartość stanu konta
- dopisz do klasy *Macs* metodę *update_portfolio()*, która przyjmuje argument *money* i dopisuje go do listy *portfolio*\
<!-- End of list -->
Na tym etapie program powinien zapisywać na bieżąco wszystkie zmieny stanu konta.
### 1.2
Czas poszerzyć metodę *raport* klasy *Macs* o możliwość raportowania stanu konta:
- dodaj do DataFramu *df* kolumnę *Poftfolio* i pszechowaj w niej zmienną *portfolio*
- do *fig* dodaj subplot, który narysuje wykres zmian w portfolio.

# Zadanie 2
Aktualnie program zarabia pieniądze otwierając pozycję *buy* przy niskiej cenie i zamykając pozycję *buy* przy wysokiej cenie. Zmodyfikuj program tak, aby możeliwe było zarabianie poprzez otwarcie pozycji *sell* przy wysokiej cenie i zamknięcie pozycji *sell* przy niższej cenie.\
Program podejmuje decyzje o otwarciu i zamknięciu pozycji w metodzie *transaction()* klasy *DataStorage* na podstawie sygnałów przesłanych przez klasę *Macs*.\
Przeanalizuj działanie metod *transaction(), buy()* oraz *sell()*. Napisz nowe metody umożliwiające zarabianie na spadkach.\
Przeczytaj dokumentację komendy *tradeTransaction* dostępnej pod linkiem:\
http://developers.xstore.pro/documentation/#tradeTransaction
oraz zapoznaj się z plikiem *xAPIConnector.py*, znajdują się tam klasy, które mogą pomóc przy ustawianiu argumentów komendy *tradeTransaction*.\
**Uwaga!** Jako wolumen transakcji ustaw warość 1. Zwróć również uwagę na cenę, którą należy podać (ask lub bid price).
