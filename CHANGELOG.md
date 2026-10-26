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

## 2026-10-26 — końcowa kontrola i uzupełnienie projektu

- Porównano projekt z wymaganiami PDF i uruchomiono zastane testy (17 OK, 1 błąd).
- Naprawiono dane wejściowe testu procesu PDF bez osłabiania walidacji dokumentów.
- Wydzielono validate, dodano kontrolę pustych wyborów, logowanie błędów i czasu,
  komunikaty o uprawnieniach oraz obsługę braku ekranu przy starcie GUI.
- Dodano testy końcowe i integracyjne. Wynik: 28 OK, bez pominięć w środowisku testowym.
- Wygenerowano aktualne dowody ośmiu konwersji, raport, tabelę zgodności i przewodnik obrony.
- Uaktualniono README i przygotowano czysty pakiet bez cache i starych wyników.

To wpis rzeczywiście wykonanej weryfikacji. Starsze wpisy zachowano z wejściowego ZIP-a;
nie odtwarzano fikcyjnych commitów ani nie potwierdzano terminowości wcześniejszych laboratoriów.

## 2026-10-26 — uporządkowanie pakietu według PDF

- Przeniesiono raport i przewodnik obrony do docs/; README zawiera kompletną
  instrukcję, macierz par, ograniczenia, oczekiwane wyniki i źródła.
- Usunięto osobną tabelę zgodności dublującą README oraz surowe logi testów.
- Ograniczono dowody do JSON, DOCX, ODT i dwóch PDF; usunięto kopie wejść
  oraz tekstowe zrzuty PDF. Nazwy PDF wskazują format źródłowy.
- Uporządkowano nazwy modułów testowych i usunięto cztery powtarzające się
  przypadki; pozostałe 24 testy przeszły bez pominięć, w tym GUI i PDF.
- Rozszerzono .gitignore o logi i pliki systemowe. Historia Git została zachowana.
