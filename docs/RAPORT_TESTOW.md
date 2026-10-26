# Raport testów — 26.10.2026

## Wynik i odtworzenie

Po uporządkowaniu zestawu: **24 testy OK, 0 pominiętych**.
Usunięto cztery przypadki dublujące CSV/JSON i walidację ścieżek;
pokrycie tych zachowań zachowano w `tests/test_core.py`.

Polecenie: `python -m unittest discover -s tests -v`.
Środowisko: Linux, Python 3.12.14, python-docx 1.2.0,
LibreOfficeDev 26.8.0.0.alpha0, Tk 9.0; GUI na ekranie Xvfb.
Testy uruchomiono w osobnym venv z zależnościami z `requirements.txt`.
Wcześniejsza weryfikacja instalacji od zera również zakończyła się powodzeniem.
Surowych logów testów nie przechowuje się w repozytorium; można je odtworzyć
powyższym poleceniem. Bez LibreOffice lub ekranu odpowiednie testy są pomijane.

## Minimalna macierz testów

| Przypadek | Wynik i dowód |
|---|---|
| Grupa A: CSV↔JSON | Round-trip zachowuje kolejność kolumn, BOM na wejściu, polskie znaki, puste pola, przecinki i wielowierszowe wartości; test_core.py i dowody/dane.json |
| Grupa B: TXT↔DOCX/ODT | Identyczny tekst po konwersji w obie strony; puste akapity, spacje i tabulatory; test_documents.py i dowody/tekst.docx, tekst.odt |
| Grupa C: DOCX/ODT→PDF | Rzeczywiste PDF; sprawdzono nagłówek i polskie zdanie przez pdftotext; test_integration.py i dowody/z-docx.pdf, z-odt.pdf |
| Błędne lub uszkodzone wejście | Kontrolowane błędy JSON, CSV, kodowania i dokumentu; uszkodzony DOCX/ODT nie uruchamia procesu |
| Nieobsługiwana para | execute odrzuca żądanie; GUI usuwa formaty i blokuje przycisk |
| Brak biblioteki/programu | Symulowany brak python-docx i błędna ścieżka LibreOffice; komunikaty z instrukcją rozwiązania |
| Konflikt nazwy | Oryginał zachowany, wynik z przyrostkiem, również w GUI |
| Walidacja i zapis | Puste wybory, brak pliku/katalogu oraz symulowana odmowa zapisu; brak pliku wynikowego po błędzie |
| Proces zewnętrzny | Kod 7, brak PDF przy kodzie 0, timeout, błąd startu i shell=False |
| Logowanie i CLI | Potwierdzony zapis przyczyny błędu; błędny JSON w CLI daje kod 1, bez tracebacku w stderr |
| GUI | Rzeczywiste widgety: dynamiczne formaty, blokada podczas pracy, wynik/błąd oraz bezpieczne nazwy |

Pliki wejściowe są w `examples/`, a minimalny zestaw wyników opisano w
[dowody/README.md](../dowody/README.md). Testy tworzą własne dane tymczasowe.
Scenariusz ręcznej demonstracji: [OBRONA.md](OBRONA.md).

## Ograniczenia weryfikacji

Nie testowano Windows/macOS ani wizualnej zgodności złożonych układów.
Odmowę zapisu sprawdzono przez symulację, nie na wszystkich systemach plików.
W testach GUI modalne komunikaty zastąpiono atrapami.
