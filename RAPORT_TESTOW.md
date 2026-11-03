# Raport testów

## Weryfikacja z 30.10.2026

## Środowisko i wykonanie

Windows; Python 3.12.14; python-docx 1.2.0; LibreOffice 26.8.1.1 bf6ef2662401c7d6dce671ab4deb26ee0af3a7c1.
Polecenie: `python -m unittest discover -s tests -v`.
Wynik: **23 testy, wszystkie OK**; powtórzono także na kodzie rozpakowanym z finalnego ZIP-a.
W środowisku analizy TEMP/TMP i LOCALAPPDATA wskazywały katalogi robocze z prawem zapisu.
Nie jest to wymagana konfiguracja zwykłej instalacji.

## Minimalna macierz

| Przypadek | Wynik i dowód |
|---|---|
| Poprawne dane w każdej grupie | Wykonano wszystkie 8 kierunków; wejścia w examples, wyjścia w dowody |
| Błędna treść | Testy błędnego CSV/JSON, kodowania i uszkodzonego ODT; GUI przekazuje błąd |
| Nieobsługiwana para | Testy execute i próba GUI: pusta lista oraz zablokowany przycisk |
| Brak LibreOffice | Test nieistniejącej ścieżki konfiguracji, kontrolowany komunikat |
| Brak python-docx | Symulowany ImportError po rozpakowaniu finalnego ZIP-a: instrukcja pip install, próba OK |
| Konflikt nazwy | Test zachowuje oryginał i sprawdza przyrostek _1 |
| Polskie znaki i puste pola | Testy CSV/JSON i konwersje zwrotne TXT/DOCX/ODT |
| Proces zewnętrzny | Osobne testy kodu 7, braku PDF i timeoutu; shell=False, limit 60 s |
| Uprawnienia | Symulowany PermissionError: czytelny komunikat; nie wykonano próby na rzeczywistym katalogu tylko do odczytu |
| Logowanie | Test potwierdza zapis wyjątku do logu; aplikacja używa rotacji |

## Rzeczywiste wyniki

CSV → JSON i JSON → CSV wykonane. TXT → DOCX → TXT oraz TXT → ODT → TXT:
porównanie tekstów identyczne. DOCX → PDF i ODT → PDF utworzyły otwieralne pliki.
PDFium potwierdził frazy z polskimi znakami, a render obu PDF sprawdzono wizualnie.
Złożone formatowanie i duże pliki nie były przedmiotem tej próby.

## Próba GUI

Utworzono rzeczywiste widgety Tkinter, wybrano ścieżki przez StringVar i wywołano
convert(), obsługując pętlę zdarzeń. Sprawdzono listę dla CSV, wynik sukcesu,
wynik błędu dla bledny.json i blokadę nieobsługiwanego pliku.
Wywołania messagebox zastąpiono mockami, aby automatyczna próba nie czekała na kliknięcie.
Nie jest to pełna ręczna demonstracja obsługi okien dialogowych.

## Odtwarzanie i ograniczenia

Projekt ma README, zależności, 4 dane wejściowe, macierz z ograniczeniami,
raport, źródła i deklarację AI oraz dziennik prac.
Nie instalowano od zera całego środowiska wirtualnego; użyto dostępnego runtime.
Linux i macOS nie były testowane. Historycznych etapów pracy i terminów nie można
potwierdzić zawartością ZIP-a.
Wersja paczki jest oczyszczona z cache, starych powielonych wyników i środowiska.

## Ponowna kontrola - 03.11.2026

Po uporządkowaniu dokumentacji wykonano ponownie:
`python -m unittest discover -s tests -v`.
Wynik: **23 testy, wszystkie OK** (Windows, dostępny runtime Python).
Kod aplikacji i testy są identyczne z wejściowym archiwum; zmiany dotyczą dokumentacji.

Sprawdzono kompletność paczki względem instrukcji projektu: kod, osiem kierunków
z trzech grup, GUI, README, requirements.txt, cztery wejścia przykładowe,
opisy wyników, testy automatyczne, raport, źródła, deklaracja AI i dziennik zmian.

Ta kontrola nie obejmowała ponownej demonstracji GUI, rzeczywistych konwersji PDF
ani czystej instalacji. Wcześniejsze wyniki tych prób opisano wyżej.
Historia etapów i termin oddania nie mogą być potwierdzone samą zawartością paczki.
