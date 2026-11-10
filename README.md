# Uniwersalny konwerter plików - Projekt 1

Autor: **Szymon Głogowski**.
Aplikacja desktopowa w Pythonie z GUI Tkinter/ttk i dodatkowym interfejsem konsolowym.
Obsługuje osiem kierunków konwersji danych i dokumentów z trzech grup.

## Instalacja

Wymagania: Python 3.10+ z Tkinter/ttk, python-docx (requirements.txt).
LibreOffice jest wymagany dla obu kierunków do PDF; pozostałe konwersje go nie potrzebują.

Polecenia uruchamiaj w wypakowanym katalogu projektu, zawierającym README.md.

Windows (PowerShell), bez potrzeby aktywacji środowiska:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m converter
```

Przy kolejnych uruchomieniach wystarczy ostatnie polecenie.
W przykładach poniżej zastąp `python` przez `.\.venv\Scripts\python.exe`,
jeżeli środowisko nie jest aktywowane.

Linux/macOS:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Przykłady uruchomienia z konsoli (w aktywnym środowisku lub z jego interpreterem).
Najpierw utwórz katalog wyników:

```sh
python -c "from pathlib import Path; Path('wyniki').mkdir(exist_ok=True)"
```

```sh
python -m converter --list
python -m converter examples/dane.csv json -o wyniki
python -m converter examples/dane.json csv -o wyniki
python -m converter examples/tekst.txt docx -o wyniki
python -m converter wyniki/tekst.docx txt -o wyniki
python -m converter examples/tekst.txt odt -o wyniki
python -m converter wyniki/tekst.odt txt -o wyniki
```

Demonstracja narzędzia zewnętrznego po zainstalowaniu LibreOffice:

```sh
python -m converter wyniki/tekst.docx pdf -o wyniki
python -m converter wyniki/tekst.odt pdf -o wyniki
```

Program szuka LibreOffice w PATH i typowych lokalizacjach Windows/macOS.
Można ustawić `LIBREOFFICE_PATH` na pełną ścieżkę do soffice/soffice.com.
PowerShell: `$env:LIBREOFFICE_PATH = 'C:\Program Files\LibreOffice\program\soffice.com'`.
Brak programu daje kontrolowany błąd i kod zakończenia 1.

## Interfejs graficzny

Uruchomienie (także z CMD w Windows):

```sh
python -m converter
```

Można również użyć `python -m converter --gui`. Dotychczasowe komendy CLI nadal działają.
Wybierz plik, istniejący katalog zapisu i format z listy, a następnie kliknij **Konwertuj**.
Lista formatów korzysta z rejestru i pokazuje wyłącznie dozwolone kierunki dla rozszerzenia wejścia.
Przycisk jest zablokowany, dopóki wybory nie są poprawne. Konwersja działa w osobnym wątku;
interfejs pokazuje postęp, wynik lub czytelny błąd. Podczas pracy wybory są zablokowane.
Istniejące pliki nie są nadpisywane — wynik dostaje przyrostek `_1`, `_2` itd.

Tkinter jest składnikiem standardowej instalacji Pythona w Windows (opcja Tcl/Tk).
Na Linux może wymagać pakietu `python3-tk`. GUI wymaga środowiska graficznego.
PDF wymaga zainstalowanego LibreOffice, tak samo jak w CLI. W CMD można ustawić:

```bat
set "LIBREOFFICE_PATH=C:\Program Files\LibreOffice\program\soffice.com"
python -m converter
```

Do demonstracji: wybierz `examples/dane.csv`, sprawdź, że lista zawiera tylko `.json`,
wykonaj konwersję i otwórz wynik we wskazanym katalogu. Powtórz operację, aby zobaczyć
bezpieczny przyrostek nazwy. Wybierz `examples/tekst.txt`, aby pokazać zmianę listy na
`.docx` i `.odt`. `examples/bledny.json` pozwala pokazać kontrolowany błąd.

## Macierz formatów

| Wejście | Wyjście | Ograniczenia |
|---|---|---|
| CSV | JSON | Przecinek, pierwszy wiersz to niepuste unikalne nagłówki, minimum jeden rekord |
| JSON | CSV | Niepusta lista niepustych obiektów, jednakowe klucze, wartości wyłącznie tekstowe |
| TXT | DOCX | Linia tekstu staje się akapitem, także pusta |
| DOCX | TXT | Akapity głównej treści, bez tabel, nagłówków, przypisów i formatowania |
| TXT | ODT | Linie jako akapity, zachowane spacje i tabulatory |
| ODT | TXT | Akapity i nagłówki treści, także z tabel; bez układu tabel i formatowania |
| DOCX | PDF | Wymaga LibreOffice; układ zależy m.in. od czcionek |
| ODT | PDF | Wymaga LibreOffice; układ zależy m.in. od czcionek |

Tekst: UTF-8, na wejściu dopuszczalny BOM. Kolejność kolumn pochodzi z nagłówka CSV lub pierwszego obiektu JSON. Puste wartości to `""`; null, liczby, listy i obiekty jako wartości są odrzucane. CSV bez rekordów jest odrzucany, ponieważ pusta lista JSON nie zachowałaby nagłówków.
Katalog wyjściowy musi istnieć. Konflikt nazw daje bezpieczny przyrostek `_1`, `_2` itd.; istniejące pliki nie są nadpisywane.

## Dane przykładowe

`examples/dane.csv` i `examples/dane.json`: polskie znaki, puste pole i przecinek w wartości.
`examples/tekst.txt`: tekst z polskimi znakami oraz pustym akapitem.
`examples/bledny.json`: niepoprawny JSON do sprawdzenia komunikatu błędu.

Reguła akapitów TXT: podział po `\n`; każda część, również pusta i końcowa,
staje się akapitem dokumentu.

## Oczekiwane wyniki przykładów

- `dane.csv` → JSON: lista obiektów, nagłówki jako klucze, tekst i puste wartości zachowane.
- `dane.json` → CSV: nazwy i kolejność kolumn z pierwszego obiektu, separator przecinek.
- `tekst.txt` → DOCX/ODT: każda linia jako akapit, polskie litery zachowane;
  konwersja zwrotna odtwarza tekst bez formatowania.
- `bledny.json` → CSV: kontrolowany komunikat z linią i kolumną, bez wyniku.
- DOCX/ODT → PDF: otwieralny PDF z treścią; wymagany LibreOffice i właściwe czcionki.

## Testowanie i dziennik błędów

Uruchom: `python -m unittest discover -s tests -v`.
Aktualne wyniki i ograniczenia weryfikacji: `RAPORT_TESTOW.md`.
Błędy konwersji są zapisywane z tracebackiem w UTF-8:
- Windows: `%LOCALAPPDATA%/PVConverter/converter.log`;
- przy braku LOCALAPPDATA: `~/.local/state/PVConverter/converter.log`.
Log ma limit 1 MB i dwie kopie rotacyjne. Powstaje przy pierwszym błędzie.
Brak możliwości zapisu logu nie blokuje obsługi pierwotnego błędu.
Log może zawierać ścieżki plików.
GUI pokazuje pary z rejestru. Dostępność LibreOffice i python-docx jest sprawdzana
przy wykonywaniu odpowiedniego kierunku; brak zależności daje instrukcję rozwiązania.

## Architektura

`converter/core.py`: rejestr dekoratorów, konwertery, walidacja, wyjątek `ConversionError`.
`converter/__main__.py`: argumenty CLI i komunikaty. `converter/gui.py`: okno Tkinter/ttk korzystające z `available_targets()` i `execute()`; kolejka przekazuje wynik z wątku roboczego do głównego wątku GUI.
Dodanie kierunku: funkcja z dekoratorem `@converter('.wejście', '.wyjście')`.
DOCX obsługuje python-docx, ODT standardowe ZIP/XML, dane standardowe csv/json.

Proces PDF: wykrycie programu, osobny profil LibreOffice, lista argumentów w `subprocess.run`, `shell=False`, limit 60 s, sprawdzenie kodu zakończenia, istnienia i nagłówka PDF. Konwersja odbywa się w katalogu tymczasowym przed bezpiecznym zapisaniem wyniku.

## Struktura projektu

- `converter/` - kod aplikacji: konwertery, GUI i obsługa konsoli.
- `examples/` - cztery wejściowe pliki demonstracyjne.
- `tests/` - testy automatyczne.
- `dowody/` - zachowane wyniki konwersji; opis w [dowody/README.md](dowody/README.md).
- `requirements.txt` - zależności instalowane przez pip.
- [RAPORT_TESTOW.md](RAPORT_TESTOW.md) - wyniki oraz ograniczenia weryfikacji.
- [CHANGELOG.md](CHANGELOG.md) - dziennik prac i historia zmian.

README opisuje aktualną wersję. Historyczne etapy opisano wyłącznie w CHANGELOG.md.

## Źródła i autorstwo
Autor: **Szymon Głogowski**.
- Zakres: dostarczony `projekt-1-konwerter (2).pdf`.
- Python: https://docs.python.org/3/library/csv.html, https://docs.python.org/3/library/json.html, https://docs.python.org/3/library/subprocess.html
- Tkinter: https://docs.python.org/3/library/tkinter.html
- python-docx: https://python-docx.readthedocs.io/
- ODF: https://docs.oasis-open.org/office/v1.2/os/OpenDocument-v1.2-os-part1.html
- LibreOffice: https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html
- Pomoc AI: kod i dokumentacja przygotowane z pomocą OpenAI Codex.

Pomoc AI przy aktualizacji 30.10.2026: OpenAI Codex - przegląd wymagań,
naprawa testów procesu, logowanie błędów, dokumentacja i sprawdzenie konwersji.

Pomoc AI przy aktualizacji 03.11.2026: OpenAI Codex - uporządkowanie dokumentacji,
porównanie kompletności paczki z instrukcją i ponowne uruchomienie testów.

