# Raport testów — 2026-10-14

Polecenie: `python -m unittest discover -s tests -v`.
Wynik: 8 testów, wszystkie OK.

| Test | Wynik |
|---|---|
| CSV → JSON → CSV, UTF-8, puste wartości, przecinki, konflikt nazwy | OK |
| Niepoprawny JSON, różne klucze, null, powtórzony klucz | Kontrolowany błąd |
| Powtórzone nagłówki CSV, brak pól, brak rekordów | Kontrolowany błąd |
| TXT → DOCX → TXT, polskie znaki i puste akapity | Treść identyczna |
| TXT → ODT → TXT, spacje, tabulatory, polskie znaki | Treść identyczna |
| Brak wejścia, katalogu, nieobsługiwana para, formaty dla TXT | OK |
| Brak LibreOffice przez nieistniejącą ścieżkę konfiguracji | Czytelny błąd |
| Kod procesu 7, brak PDF mimo kodu 0, timeout | Kontrolowane błędy; shell=False |

## Rzeczywiste konwersje PDF

Doinstalowano lokalnie LibreOffice Writer 25.2.3.2 w `/workspace/lo-runtime` (bez zmian katalogów systemowych). Wykonano przez CLI projektu:

- DOCX → PDF: `examples/wyniki/tekst.pdf` — kod procesu 0, poprawny PDF.
- ODT → PDF: `examples/wyniki/tekst_1.pdf` — kod procesu 0, poprawny PDF.

Odczyt obu plików przez `pdftotext` potwierdził tekst „Zażółć gęślą jaźń.” oraz „Drugi akapit: Łódź, Kraków i Warszawa.”, z poprawnymi polskimi znakami. Wszystkie osiem kierunków wykonano rzeczywiście. Nie oceniano wizualnej zgodności złożonego formatowania. Po instalacji ponownie wykonano 8 testów automatycznych — wszystkie OK.

Lokalny launcher: `/workspace/lo-runtime/bin/libreoffice`; zmienna `LIBREOFFICE_PATH` wskazuje ten plik. Ze względu na izolację środowiska wykonanie LibreOffice wymagało uruchomienia poza ograniczeniami sandboxa. Lokalny runtime nie jest częścią paczki do oddania; na własnym komputerze należy zainstalować LibreOffice zgodnie z README.
