# Uniwersalny konwerter plików

Aplikacja Python 3 + Tkinter/ttk realizująca projekt „Programowanie V”.
Obsługuje osiem kierunków z trzech grup: dane (A), tekst/dokumenty (B)
i dokumenty/PDF (C). Udostępnia GUI oraz CLI.

## Wymagania i instalacja

Python 3.10+, Tkinter, python-docx oraz LibreOffice Writer do obu konwersji PDF.
LibreOffice jest osobnym programem i nie jest instalowany przez pip.

```sh
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell zamiast powyższej linii:
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m converter
```

Debian/Ubuntu: `sudo apt install python3-tk libreoffice-writer fonts-dejavu`.
Windows: instalator Pythona z opcją Tcl/Tk oraz [LibreOffice](https://www.libreoffice.org/download/download-libreoffice/).
macOS: Python z działającym Tkinterem i LibreOffice w katalogu Applications.
GUI wymaga sesji graficznej. Bez ekranu można korzystać z CLI.

Program szuka LibreOffice w PATH i typowych lokalizacjach Windows/macOS.
Można ustawić `LIBREOFFICE_PATH` na plik wykonywalny:

```powershell
$env:LIBREOFFICE_PATH = 'C:\Program Files\LibreOffice\program\soffice.com'
```

Brak zależności daje komunikat z instrukcją rozwiązania; CLI zwraca kod 1.

## Obsługa

W GUI wybierz istniejący plik wejściowy, katalog zapisu i format docelowy.
Lista formatów zależy od rozszerzenia. Przycisk **Konwertuj** jest dostępny
po poprawnym wyborze; konwersja działa w tle, a okno pokazuje status i wynik
lub komunikat błędu. Dostępne jest też `python -m converter --gui`.

Przykłady CLI (wykonywane w katalogu projektu):

```sh
python -c "from pathlib import Path; Path('wyniki').mkdir(exist_ok=True)"
python -m converter --list
python -m converter examples/dane.csv json -o wyniki
python -m converter examples/dane.json csv -o wyniki
python -m converter examples/tekst.txt docx -o wyniki
python -m converter examples/tekst.txt odt -o wyniki
python -m converter wyniki/tekst.docx txt -o wyniki
python -m converter wyniki/tekst.odt txt -o wyniki
python -m converter wyniki/tekst.docx pdf -o wyniki
python -m converter wyniki/tekst.odt pdf -o wyniki
```

Istniejące pliki są zachowywane. Nowy wynik otrzymuje przyrostek `_1`, `_2` itd.
Katalog wyjściowy musi istnieć i pozwalać na zapis.

## Obsługiwane pary i ograniczenia

| Grupa | Wejście | Wyjście | Semantyka i ograniczenia |
|---|---|---|---|
| A | CSV | JSON | Przecinek; pierwszy wiersz to niepuste, unikalne nagłówki; minimum jeden rekord |
| A | JSON | CSV | Niepusta lista niepustych obiektów, te same klucze, wartości wyłącznie tekstowe |
| B | TXT | DOCX | Każda linia, również pusta i końcowa, staje się akapitem |
| B | DOCX | TXT | Akapity głównej treści; bez tabel, nagłówków strony, przypisów i formatowania |
| B | TXT | ODT | Linie jako akapity; zachowanie spacji i tabulatorów |
| B | ODT | TXT | Akapity i nagłówki treści, także z tabel; bez układu tabel i formatowania |
| C | DOCX | PDF | LibreOffice; wygląd zależy od czcionek i wersji programu |
| C | ODT | PDF | LibreOffice; wygląd zależy od czcionek i wersji programu |

Tekst jest zapisywany jako UTF-8; na wejściu dopuszczalny BOM.
Kolejność kolumn pochodzi z nagłówków CSV lub pierwszego obiektu JSON.
Puste pola to `""`; liczby, null, listy i obiekty jako wartości są odrzucane.
Tekstowe wartości chronią np. zera wiodące kodów. CSV bez rekordów jest
odrzucany, ponieważ pusta lista JSON nie zachowałaby nagłówków.
Konwersje tekstowe nie zachowują złożonego formatowania, makr ani wykresów.

## Przykłady i oczekiwane wyniki

| Dane wejściowe | Oczekiwany rezultat |
|---|---|
| examples/dane.csv | JSON z tymi samymi nagłówkami, polskimi znakami, pustym polem i przecinkiem w wartości |
| examples/dane.json | CSV z kolumnami w kolejności pierwszego obiektu i wartościami tekstowymi |
| examples/tekst.txt | DOCX/ODT z polskimi znakami i pustym akapitem; po powrocie do TXT identyczny tekst |
| examples/bledny.json | Kontrolowany błąd z linią i kolumną; brak pliku wynikowego |

Minimalne pliki dowodowe i ich opis: [dowody/README.md](dowody/README.md).
Własne wyniki zapisuj w ignorowanym przez Git katalogu `wyniki/`.

## Architektura i błędy

`converter/core.py` zawiera rejestr dekoratorów, walidację, konwertery i wspólny
wyjątek `ConversionError`. `gui.py` obsługuje wyłącznie interfejs, wątek roboczy
i kolejkę wyników; `__main__.py` uruchamia CLI lub GUI. Nowa funkcja z dekoratorem
`@converter('.wejście', '.wyjście')` automatycznie uzupełnia listę GUI.

Dane obsługują standardowe csv/json, DOCX biblioteka python-docx, ODT standardowe
ZIP/XML. LibreOffice działa z osobnym profilem, listą argumentów, `shell=False`
i limitem 60 s. Sprawdzane są kod zakończenia i wynik PDF. Konwersja powstaje
najpierw w katalogu tymczasowym; finalna nazwa jest tworzona z trybem `xb`.

Po uruchomieniu przez `python -m converter` błędy z tracebackiem i czas operacji
trafiają do `pv-converter.log` w katalogu tymczasowym systemu. Jego lokalizację
pokaże `python -c "import tempfile; print(tempfile.gettempdir())"`.
Przy braku możliwości utworzenia logu program korzysta z konsoli.

## Testy i dokumentacja

```sh
python -m unittest discover -s tests -v
```

Testy nie wymagają pytest. Test rzeczywistych PDF wymaga LibreOffice;
testy GUI wymagają Tkinter i ekranu. Brak zależności systemowej oznacza jawne
pominięcie odpowiedniego testu. Linux bez pulpitu: po instalacji `xvfb` i `xauth`
użyj `xvfb-run -a python -m unittest discover -s tests -v`.

- [Raport testów](docs/RAPORT_TESTOW.md): wynik, minimalna macierz i ograniczenia weryfikacji.
- [Przewodnik do obrony](docs/OBRONA.md): przepływ, decyzje i scenariusz demonstracji.
- [Dziennik prac](CHANGELOG.md): etapy i późniejsze zmiany; historia jest też w Git.

Struktura: `converter/` — kod; `tests/` — testy; `examples/` — wejścia;
`dowody/` — mały zestaw wyników; `docs/` — dokumentacja dodatkowa.
Repozytorium nie zawiera środowiska wirtualnego, cache ani surowych logów testów.

## Autorstwo i źródła

Autor/student: **Szymon Głogowski**. Kod i dokumentacja powstały z pomocą
**OpenAI Codex**; osoba oddająca projekt powinna rozumieć wykorzystany kod.

- Zakres: dostarczony PDF „Projekt 1. Uniwersalny konwerter plików”.
- Python: [csv](https://docs.python.org/3/library/csv.html), [json](https://docs.python.org/3/library/json.html), [subprocess](https://docs.python.org/3/library/subprocess.html).
- [Tkinter](https://docs.python.org/3/library/tkinter.html).
- [python-docx](https://python-docx.readthedocs.io/).
- [ODF 1.2](https://docs.oasis-open.org/office/v1.2/os/OpenDocument-v1.2-os-part1.html).
- [Parametry LibreOffice](https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html).
