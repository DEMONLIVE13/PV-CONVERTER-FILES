# Uniwersalny konwerter plików — laboratorium 2

Etap projektu z „Programowania V”, zgodny z tabelą kamieni milowych w `projekt-1-konwerter.pdf`. Działające konwersje **CSV → JSON i JSON → CSV bez GUI**. Tkinter i formaty biurowe są etapami kolejnych laboratoriów, a nie funkcjami tej wersji.

## Wymagania i uruchomienie

Python **3.10 lub nowszy** na Windows, Linux lub macOS. Brak zależności zewnętrznych; `requirements.txt` dokumentuje ten fakt. Polecenia wykonuj w katalogu projektu. Na Windows można zastąpić `python` przez `py -3`, a na Linux/macOS przez `python3`.

```sh
python --version
python -m konwerter --lista
python -m konwerter dane/osoby.csv --format json --katalog wyniki
python -m konwerter dane/produkty.json --format csv --katalog wyniki
python -m konwerter dane/bledny.json --format csv --katalog wyniki
python -m unittest discover -s tests -v
```

Katalog `wyniki` jest dołączony. Dla własnego katalogu utwórz go wcześniej (`mkdir moj_katalog`). Ścieżki ze spacjami podawaj w cudzysłowach. Sukces: komunikat ze ścieżką i kod zakończenia 0. Błąd danych lub plików: czytelny komunikat na stderr i kod 1. Brak argumentów: pomoc argparse i kod 2.

## Format danych i ograniczenia

- CSV: UTF-8 (wejście może mieć BOM), separator **przecinek**, pierwszy wiersz to nagłówki. Standardowe cytowanie CSV obsługuje przecinki, cudzysłowy i nowe linie wewnątrz pól.
- Nazwy kolumn muszą być unikalne i niepuste (także nazwa z samych spacji jest błędem). Każdy rekord musi mieć tyle pól, ile nagłówek. Pusty wiersz w CSV jest błędem; puste pole w rekordzie jest poprawne.
- JSON: **niepusta lista obiektów o tych samych kluczach**. Wszystkie wartości są tekstami. Pusta wartość to `""`, nie `null`. Liczby, booleany, zagnieżdżone obiekty/listy, NaN i powtórzone klucze są odrzucane. Wartości liczbowe zapisz jako tekst, np. `"0012"`.
- Kolejność rekordów i nazwy kolumn zostają zachowane. Kolejność kolumn w CSV pochodzi z pierwszego obiektu JSON; kolejność kluczy w dalszych obiektach może się różnić.
- Wyniki: UTF-8 bez BOM, polskie znaki w JSON są czytelne. Nie gwarantujemy identycznych bajtów CSV (cytowanie i końce linii mogą się zmienić), ale zachowujemy wartości pól.
- CSV bez rekordów i pusta lista JSON są odrzucane: lista rekordów nie przechowałaby nagłówków pustej tabeli.
- Pliki są przetwarzane w pamięci: wersja przeznaczona do małych danych laboratoryjnych.
- Wynik zapisuje się jako `nazwa.json` lub `nazwa.csv`; konflikt daje `nazwa_1`, `nazwa_2` itd. Bez nadpisywania, także przy równoczesnym tworzeniu wyniku. Błąd danych nie tworzy pliku wynikowego.

Przykład akceptowanego JSON:

```json
[
  {"imię": "Łukasz", "kod": "0012", "uwagi": ""},
  {"imię": "Zośka", "kod": "0013", "uwagi": "Łódź"}
]
```

## Macierz konwersji

| Wejście | Wyjście | Stan | Ograniczenia / narzędzie |
|---|---|---|---|
| CSV | JSON | działa, lab 2 | tabela z nagłówkiem i co najmniej jednym rekordem |
| JSON | CSV | działa, lab 2 | lista jednorodnych obiektów z wartościami tekstowymi |
| TXT | DOCX | plan, lab 3 | python-docx; akapity, bez złożonego formatowania |
| DOCX | TXT | plan, lab 3 | python-docx; tekst akapitów, bez obrazów |
| DOCX | PDF | plan, lab 3–5 | LibreOffice headless; zależność systemowa |
| ODT | PDF | plan, lab 3–5 | LibreOffice headless; układ może się zmienić |

TXT jest reprezentowany przez `dane/notatka.txt`; na lab 2 nie wymyślamy dodatkowej konwersji TXT, której kamień milowy nie wymaga. Plan obejmuje łącznie sześć kierunków z trzech grup. GUI z dynamiczną listą formatów przewidziano na lab 4, pełną walidację i oddanie na lab 5.

## Struktura i przepływ

`konwerter/core.py`: model żądania, walidacja, rejestr, konwertery i zapis. `konwerter/__main__.py`: wyłącznie obsługa konsoli. Nową parę dodaje się funkcją oznaczoną dekoratorem `@converter`; CLI korzysta ze wspólnego rejestru. `available_targets()` będzie użyteczne przy budowie GUI.

Przepływ: argumenty → `ConversionRequest` → walidacja pliku/katalogu/pary → konwersja w pamięci → bezpieczna nazwa i zapis → status. `ConversionError` przenosi zrozumiałe komunikaty; błędny JSON zawiera numer linii i kolumny. Brak możliwości zapisu jest wykrywany podczas rzeczywistego otwierania pliku, zamiast zawodnego sprawdzania samych uprawnień.

## Dane do demonstracji

| Plik | Oczekiwany wynik |
|---|---|
| `dane/osoby.csv` | dwa obiekty JSON, polskie znaki, puste uwagi i przecinek w polu |
| `dane/produkty.json` | nagłówek `nazwa,cena,opis`, dwa rekordy, puste pole |
| `dane/bledny.json` | kontrolowany błąd składni, bez pliku wynikowego |
| `dane/notatka.txt` | materiał do przyszłych konwersji tekstowych, dwa akapity |

Przykładowe poprawne wyniki są w `wyniki`. Raport: `RAPORT_TESTOW.md`. Dziennik prac: `CHANGELOG.md`.

## Autorstwo, źródła i AI

Autor/student: **Szymon Głogowski**. Implementacja została przygotowana z pomocą **OpenAI Codex (AI)** na podstawie załączonej instrukcji projektu. Student powinien rozumieć kod i potrafić zmienić go podczas obrony. ZIP `File_Converter-main.zip` podano jako inspirację, ale nie został odczytany z powodu limitu transferu 32 MiB; kod z niego nie był kopiowany.

Źródła: `projekt-1-konwerter.pdf`, wersja 5 października 2026; oficjalne dokumentacje standardowych modułów Pythona:
- https://docs.python.org/3/library/csv.html
- https://docs.python.org/3/library/json.html
- https://docs.python.org/3/library/pathlib.html
- https://docs.python.org/3/library/argparse.html
- https://docs.python.org/3/library/unittest.html

Do planowanych etapów: https://python-docx.readthedocs.io/ oraz https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html . Biblioteki te nie są instalowane ani używane na lab 2.
