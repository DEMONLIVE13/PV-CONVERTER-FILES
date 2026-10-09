# Raport testów — lab 2

Data: 2026-10-09. Środowisko wykonania: Linux, Python 3.12.14. Brak zewnętrznych zależności. Windows i macOS nie były testowane w tym środowisku.

Polecenie: `python -m unittest discover -s tests -v`.
**Wynik: 10 testów, wszystkie OK.**

| Przypadek | Sprawdzone zachowanie | Wynik |
|---|---|---|
| CSV → JSON → CSV | polskie znaki, kolejność kolumn, zera wiodące, puste pola, przecinek, nowe linie | OK |
| JSON → CSV | kolejność z pierwszego obiektu przy różnej kolejności kolejnych kluczy | OK |
| Błędny JSON | komunikat z linią i kolumną; brak wyniku | OK |
| Błędna struktura JSON | pusta lista, obiekt zamiast listy, liczby, null, różne kolumny, powtórzone klucze, NaN | OK |
| Błędny CSV | pusty plik, brak rekordów, powtórzone/puste nagłówki, zła liczba pól, niezamknięte cytowanie | OK |
| BOM i wielkie rozszerzenie | UTF-8 z BOM i `.CSV` są akceptowane | OK |
| Istniejący wynik | nowa nazwa `_1`, oryginalny plik pozostaje zachowany | OK |
| Walidacja | brak pliku, brak katalogu, nieobsługiwana para | OK |
| Rejestr | dostępne cele zależą od rozszerzenia; TXT nie oferuje celu | OK |
| Złe kodowanie | kontrolowany komunikat o UTF-8 | OK |

Dodatkowa demonstracja CLI:

```text
python -m konwerter dane/osoby.csv --format json --katalog wyniki
Gotowe. Zapisano: wyniki/osoby.json

python -m konwerter dane/produkty.json --format csv --katalog wyniki
Gotowe. Zapisano: wyniki/produkty.csv

python -m konwerter dane/bledny.json --format csv --katalog wyniki
Błąd: Błędny JSON: linia 1, kolumna 20. Popraw składnię pliku.
```

Oba poprawne wyniki ponownie odczytano modułami `json` i `csv`: po dwa rekordy. Błędny JSON zakończył CLI kodem 1, plik `bledny.csv` nie powstał. Kontrola `git diff --check` nie zgłosiła problemów.

GUI, LibreOffice i formaty biurowe są poza zakresem labu 2. Zapis w katalogu bez uprawnień nie był oddzielnie symulowany; błędy systemowe odczytu/zapisu są obsługiwane przez wspólny model błędów.
