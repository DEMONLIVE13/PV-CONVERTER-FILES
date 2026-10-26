# Raport testów — 26.10.2026

## Wynik aktualnej weryfikacji

`python -m unittest discover -s tests -v`: **28 testów, OK, 0 pominiętych**.
Pełny zapis: `testy-wynik.txt`. Weryfikacja: Linux, Python 3.12.14,
python-docx 1.2.0, LibreOfficeDev 26.8.0.0.alpha0, Tk 9.0.
Testy GUI wykonano na wirtualnym ekranie Xvfb (`DISPLAY=:107`).
LibreOffice był dostępny jako `soffice` w środowisku wykonawczym.

Raport zastępuje nieaktualny raport dołączony do wejściowego ZIP-a.
Początkowo było 18 testów, w tym jeden nieprzechodzący: test procesu PDF używał
uszkodzonego pliku ODT. Naprawiono dane wejściowe testu, zachowując walidację dokumentów.

## Minimalna macierz z PDF

| Przypadek | Dowód i rezultat |
|---|---|
| Poprawny plik w grupie A | CSV/JSON: tekst, kolejność kolumn, BOM, przecinki, wielowierszowe pola i puste wartości; round-trip OK |
| Poprawny plik w grupie B | TXT→DOCX→TXT i TXT→ODT→TXT; identyczny tekst z polskimi znakami i pustymi akapitami |
| Poprawny plik w grupie C | Rzeczywiste DOCX→PDF i ODT→PDF; nagłówek PDF oraz polskie zdanie sprawdzane przez pdftotext |
| Błędna treść | Błędny JSON ze wskazaniem miejsca, wadliwe CSV i kodowanie; brak końcowego wyniku |
| Uszkodzony dokument | DOCX/ODT odrzucone przed wywołaniem procesu |
| Nieobsługiwana para | Odrzucenie w execute; GUI usuwa formaty i blokuje przycisk |
| Brak zależności | Brak LibreOffice przez konfigurację; brak python-docx przez symulację importu; komunikaty z instrukcją |
| Konflikt nazwy | Oryginał zachowany; wynik z przyrostkiem, także w przepływie GUI |
| Brak zapisu | Symulowana odmowa utworzenia katalogu tymczasowego: kontrolowany komunikat, brak wyniku |
| Błędy procesu | Kod 7, brak PDF przy kodzie 0, timeout i błąd startu; sprawdzone shell=False |
| Puste wybory i ścieżki | Test validate oraz blokada GUI |
| Dziennik błędów | assertLogs potwierdza zapis przyczyny błędu |
| CLI | Niepoprawny JSON: kod 1, komunikat, brak tracebacku w stderr i brak wyniku |
| GUI | Dynamiczne formaty, blokada w trakcie pracy, komunikat wyniku/błędu i bezpieczne nazwy |

## Wyniki do obejrzenia

`dowody/OPIS.md` zawiera listę wszystkich ośmiu rzeczywistych konwersji,
rozmiary i opis kontroli. Katalog zawiera wejściom odpowiadające CSV, JSON,
DOCX, ODT, TXT oraz dwa PDF i tekst odczytany z PDF.

Nie testowano Windows/macOS, wizualnej zgodności złożonych układów ani
rzeczywistych praw dostępu na wszystkich systemach plików; odmowę zapisu
sprawdzono przez symulację. GUI testowano programowo z rzeczywistymi widgetami,
zastępując modalne okna komunikatów atrapami. Ręczny scenariusz jest w OBRONA.md.
W środowisku bez LibreOffice lub ekranu odpowiednie testy są jawnie pomijane.

## Odtwarzalność instalacji

Dodatkowo utworzono nowe środowisko venv poza projektem, wykonano
`python -m pip install -r requirements.txt` i uruchomiono w nim pełny zestaw:
**28 testów OK, bez pominięć**. Zapis: `testy-czyste-srodowisko.txt`.
Zależności Pythona zainstalowano od nowa; LibreOffice i ekran Xvfb pochodziły
ze środowiska systemowego testu.
