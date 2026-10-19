# Raport testów — 2026-10-19

Polecenie: `python -m unittest discover -s tests -v`.
Wynik: 18 testów, wszystkie OK, po usunięciu starego modułu testy używają `converter`.

Sprawdzono automatycznie:
- CSV/JSON: kolejność kolumn, polskie znaki, puste wartości, BOM, wielkie rozszerzenia, przecinki i wielowierszowe pola.
- Błędne dane CSV/JSON, nieprawidłowe UTF-8 i kontrolowane komunikaty.
- TXT → DOCX → TXT oraz TXT → ODT → TXT: zachowanie treści i pustych akapitów.
- Walidację ścieżek, nieobsługiwane pary i bezpieczne nazwy bez nadpisywania.
- Brak LibreOffice przez nieistniejącą ścieżkę konfiguracji.
- Symulowane błędy procesu: kod 7, brak PDF mimo kodu 0, timeout; jawne `shell=False`.

## Rzeczywiste konwersje

Python 3 i python-docx 1.2.0; LibreOfficeDev 26.8.0.0.alpha0 dostępny w PATH jako `soffice`.
Wykonano wszystkie osiem kierunków na danych z `examples` w katalogu tymczasowym:

- CSV → JSON: dane zgodne z przykładowym JSON; JSON → CSV: poprawny zapis.
- TXT → DOCX → TXT i TXT → ODT → TXT: identyczna treść wejściowa i wynikowa.
- DOCX → PDF: 11365 bajtów; ODT → PDF: 16255 bajtów.
- Odczyt obu PDF przez `pdftotext` potwierdził polskie znaki i treść akapitów.
- Błędny JSON przez CLI: kod zakończenia 1, komunikat z linią i kolumną, brak pliku wynikowego.

Wyniki generowane są podczas pracy i nie należą do kodu źródłowego. Nie oceniano wizualnej zgodności złożonego formatowania. Windows i macOS nie były testowane.
