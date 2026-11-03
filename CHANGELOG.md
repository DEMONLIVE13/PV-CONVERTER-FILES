# Dziennik prac i zmian

Poniższe historyczne wpisy zachowano z dostarczonego archiwum. Opisują kolejne
stany robocze, a nie wyłącznie zawartość obecnej paczki. Dat etapów nie potwierdzono
niezależnie. Aktualną zawartość i obsługę opisuje README.md.

## 2026-10-09 — laboratorium 2

1. Analiza kamienia milowego: dwie konwersje danych bez GUI, przykłady i macierz dalszych formatów.
2. Ustalenie semantyki: UTF-8, nagłówki CSV, lista obiektów JSON z wartościami tekstowymi.
3. Implementacja rejestru, walidacji, konwerterów, bezpiecznych nazw i CLI.
4. Dodanie danych demonstracyjnych, testów automatycznych i dokumentacji.
5. Weryfikacja konwersji oraz kontrolowanego błędu JSON; raport w osobnym pliku.

Ten wpis opisuje etap laboratorium 2.

## 2026-10-14 — lab. 3

Dodano moduł `converter` z obsługą DOCX, ODT i PDF oraz CSV/JSON,
przykłady, osiem testów i raport rzeczywistych konwersji PDF przez LibreOffice.
Zachowano wcześniejszy moduł lab. 2 i jego testy. GUI pozostaje na lab. 4.

## 2026-10-19 — weryfikacja lab. 3 i porządki

Usunięto starszy moduł konwerter, zdublowane dane i wygenerowane wyniki.
Przeniesiono testy CSV/JSON do wspólnego modułu converter i zachowano ostrą walidację CSV, nagłówków i komunikaty o błędnym JSON oraz UTF-8.
Usunięto nieaktualną ścieżkę runtime z README.

2026-10-20: próby T1–T8 z rzeczywistym LibreOffice, pliki dowodowe i odczyt PDF; walidacja uszkodzonego DOCX/ODT, obsługa błędu uruchamiania, 20 testów.

2026-10-20: uproszczono pakiet — usunięto testy, raport, skrypt demonstracyjny i wygenerowane dowody. Pozostawiono konwertery, przykładowe wejścia oraz dokumentację.

2026-10-20: lab. 4 — GUI Tkinter/ttk, wybór pliku i katalogu, dynamiczna lista formatów, walidacja, konwersja w tle, komunikaty i ochrona istniejących plików.


## 2026-10-30 - kontrola wersji końcowej

Aktualna paczka zawiera testy i raport; wcześniejszy wpis o ich usunięciu opisuje
poprzedni stan roboczy. Daty we wcześniejszych wpisach i README są deklaracjami
z dostarczonego archiwum i nie zostały niezależnie potwierdzone.
Naprawiono dane testowe procesu PDF, rozdzielono scenariusze kodu błędu,
braku PDF i timeoutu. Dodano test uszkodzonego ODT, komunikatu braku uprawnień
i zapisu logu. Dodano rotacyjny dziennik wyjątków wspólny dla GUI i CLI.
Zaktualizowano README i raport, usunięto z paczki cache i powielone wyniki.

## Wpis przeniesiony z wcześniejszego README

2026-10-14: implementacja etapu lab. 2 (CSV/JSON) i lab. 3 (DOCX/ODT/PDF), CLI i przykłady. Zapis rzeczywistych prac, nie historia wcześniejszych zajęć.

Wpis częściowo pokrywa się z etapami opisanymi wyżej; zachowano go jako zapis
źródłowy, bez tworzenia nowej wersji historii prac.

## 2026-11-03 - uporządkowanie dokumentacji

- Zastąpiono historię w README odsyłaczem do tego pliku.
- Uporządkowano sekcje README i rozdzielono instalację Windows od Linux/macOS.
- Dodano strukturę paczki i opis zachowanych wyników w dowody/README.md.
- Uzupełniono deklarację pomocy AI w dokumentacji.
- Kod aplikacji, dane przykładowe i testy pozostały bez zmian.

- Usunięto z dokumentacji porady dotyczące przygotowania do obrony.
