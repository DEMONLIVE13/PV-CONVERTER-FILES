# Raport rzeczywistych prób Lab. 3 — 2026-10-20

Środowisko: Linux, Python 3.12.14, python-docx 1.2.0,
LibreOfficeDev 26.8.0.0.alpha0 (2c87e51eeaa2b413ff4ae097b2705eea1995d8e5).
Uruchomiono `python demo_lab3.py` z LIBREOFFICE_PATH wskazującym zainstalowany
soffice; skrypt zakończył się kodem 0, komunikatem „T1–T8: OK”.
Windows/macOS oraz wizualna zgodność złożonego formatowania nie były testowane.

Każde dokładne wywołanie CLI, kod CLI i komunikat są zapisane w
[dowody_lab3/przebieg.txt](dowody_lab3/przebieg.txt).
Ścieżki /workspace w tym logu opisują środowisko wykonania; skrypt ustala je automatycznie.
Poniższe wywołania są względem katalogu repozytorium; wspólna opcja:
`-o dowody_lab3`. Skrót `converter` oznacza `python -m converter`.

| ID | Wejście i wywołanie | Oczekiwany wynik | Wynik faktyczny i dowód | Status |
|---|---|---|---|---|
| T1 | `converter examples/dane.csv json` | Dane, nagłówki, UTF-8 zgodne z przykładem | Kod 0; porównanie obiektów JSON zgodne; `dowody_lab3/dane.json` | OK |
| T2 | `converter examples/dane.json csv` | Kolejność kolumn i wartości zgodne | Kod 0; porównanie csv.reader zgodne; `dowody_lab3/dane.csv` | OK |
| T3 | `converter examples/tekst.txt docx` | Polskie znaki i puste akapity | Kod 0; DOCX odczytany python-docx; lista akapitów identyczna z TXT podzielonym po nowej linii; `dowody_lab3/tekst.docx` | OK |
| T4 | `converter dowody_lab3/tekst.docx pdf` | Rzeczywisty PDF z właściwą treścią | Kod 0; nagłówek PDF poprawny; odczyt pdftotext zgodny z tekstem po normalizacji białych znaków; `tekst.pdf`, `tekst_pdf_odczyt.txt` | OK |
| T5 | Jak T4, LIBREOFFICE_PATH ustawiony na nieistniejący plik | Błąd z instrukcją konfiguracji | Kod 1; „Nie znaleziono LibreOffice”, instrukcja instalacji lub ustawienia ścieżki; log | OK |
| T6 | `converter dowody_lab3/uszkodzony.docx pdf` (zwykły tekst) | Brak fałszywego sukcesu | Kod 1; „Uszkodzony DOCX/ODT”; brak uszkodzony.pdf; wejście i log | OK |
| T7 | Ponowne wywołanie T4 | Zachowany istniejący PDF, nowa nazwa | Kod 0; oryginalne bajty niezmienione; utworzony `tekst_1.pdf` | OK |
| T8 | `converter "dowody_lab3/dokument ze spacjami.docx" pdf` | Ścieżka przekazana jako jeden argument | Kod 0; `dokument ze spacjami.pdf` z nagłówkiem PDF | OK |

Dodatkowo `python -m unittest discover -s tests -v`: **20 testów, wszystkie OK**.
Testy procesu z atrapą: kod narzędzia 7, kod 0 bez wyniku, timeout 60 s,
nieudane uruchomienie (PermissionError); te przypadki są symulowane.
Rzeczywiste DOCX → PDF w T4/T7/T8 używa zainstalowanego LibreOffice.
Kod CLI w logu i returncode LibreOffice to dwa odrębne kody;
`office_to_pdf` sprawdza returncode narzędzia przed sprawdzeniem pliku PDF.
Wywołanie ma listę argumentów, `shell=False`, timeout 60 s, osobny profil i świeży katalog.
