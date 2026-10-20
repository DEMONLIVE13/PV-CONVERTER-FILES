# Dziennik prac

## 2026-10-09 — laboratorium 2

1. Analiza kamienia milowego: dwie konwersje danych bez GUI, przykłady i macierz dalszych formatów.
2. Ustalenie semantyki: UTF-8, nagłówki CSV, lista obiektów JSON z wartościami tekstowymi.
3. Implementacja rejestru, walidacji, konwerterów, bezpiecznych nazw i CLI.
4. Dodanie danych demonstracyjnych, testów automatycznych i dokumentacji.
5. Weryfikacja konwersji oraz kontrolowanego błędu JSON; raport w osobnym pliku.

To dziennik jednego etapu, nie historia pracy nad całym projektem. Kolejne laboratoria należy dokumentować na bieżąco.

## 2026-10-14 — lab. 3

Dodano moduł `converter` z obsługą DOCX, ODT i PDF oraz CSV/JSON,
przykłady, osiem testów i raport rzeczywistych konwersji PDF przez LibreOffice.
Zachowano wcześniejszy moduł lab. 2 i jego testy. GUI pozostaje na lab. 4.

## 2026-10-19 — weryfikacja lab. 3 i porządki

Usunięto starszy moduł konwerter, zdublowane dane i wygenerowane wyniki.
Przeniesiono testy CSV/JSON do wspólnego modułu converter i zachowano ostrą walidację CSV, nagłówków i komunikaty o błędnym JSON oraz UTF-8.
Usunięto nieaktualną ścieżkę runtime z README.

2026-10-20: próby T1–T8 z rzeczywistym LibreOffice, pliki dowodowe i odczyt PDF; walidacja uszkodzonego DOCX/ODT, obsługa błędu uruchamiania, 20 testów.

2026-10-20: uproszczono pakiet na życzenie użytkownika — usunięto testy, raport, skrypt demonstracyjny i wygenerowane dowody. Pozostawiono konwertery, przykładowe wejścia oraz dokumentację.

2026-10-20: lab. 4 — GUI Tkinter/ttk, wybór pliku i katalogu, dynamiczna lista formatów, walidacja, konwersja w tle, komunikaty i ochrona istniejących plików.
