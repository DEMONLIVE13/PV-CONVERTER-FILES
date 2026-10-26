# Przewodnik po projekcie i demonstracja

## Przepływ

1. GUI odczytuje rozszerzenie pliku i pyta available_targets o formaty z REGISTRY.
2. Po poprawnym wyborze uruchamia execute w osobnym wątku.
3. validate sprawdza ścieżki i parę formatów; rejestr wybiera funkcję.
4. Konwerter zapisuje wynik w katalogu tymczasowym wewnątrz katalogu docelowego.
5. Wynik jest kopiowany do nowego pliku otwartego z xb. Gdy nazwa istnieje,
   program zwiększa przyrostek. Błąd kopiowania usuwa częściowy plik.
6. Kolejka dostarcza wynik do głównego wątku Tkintera. root.after odbiera go,
   przywraca przyciski i pokazuje status oraz komunikat.

## Decyzje do wyjaśnienia

- JSON jest listą obiektów z tymi samymi kluczami i wartościami tekstowymi.
  Dzięki temu CSV→JSON→CSV zachowuje zera wiodące, puste pola i nazwy kolumn.
  Pusta lista JSON nie zachowuje nagłówków, dlatego jest odrzucana.
- python-docx obsługuje DOCX; ODT jest pakietem ZIP z XML. Elementy text:s i
  text:tab chronią spacje i tabulatory. Linia TXT odpowiada akapitowi.
- LibreOffice renderuje dokument do PDF. Osobny profil ogranicza konflikty z
  otwartą instancją. Nie ma shell=True; argumenty nie są interpretowane przez powłokę.
- Sam kod 0 nie gwarantuje wyniku, dlatego sprawdzamy istnienie, rozmiar i %PDF-.
- Wątek roboczy nie dotyka Tkintera. Widgety są aktualizowane w wątku głównym.
- ConversionError to błąd z komunikatem dla użytkownika; log zawiera szczegóły.

## Demonstracja (około 5 minut)

1. Uruchom `python -m converter`.
2. Wybierz examples/dane.csv i istniejący katalog zapisu. Lista ma tylko .json.
3. Wykonaj konwersję i porównaj polskie znaki, nagłówki i puste pole.
4. Powtórz — wynik ma _1, oryginał pozostaje bez zmian.
5. Wybierz examples/bledny.json — pokaż czytelny błąd, okno działa dalej.
6. Wybierz examples/tekst.txt, utwórz DOCX, a następnie PDF i otwórz go.
7. Pokaż testy i RAPORT_TESTOW.md.

## Przykładowa mała zmiana

Dodanie nowego kierunku wymaga funkcji przyjmującej source i target oraz
rejestracji dekoratorem @converter('.wejście', '.wyjście'). Funkcja ma zapisać
wynik pod dokładną ścieżką target. GUI pobierze nowy format z rejestru.
Należy też uzupełnić test, README i ograniczenia. Dodając zależność, trzeba
zapewnić kontrolowany komunikat przy jej braku.

## Granice rozwiązania

DOCX→TXT odczytuje akapity głównej treści, bez tabel i nagłówków strony.
ODT→TXT spłaszcza układ. PDF zależy od czcionek i wersji LibreOffice.
Aplikacja nie zachowuje makr ani złożonego formatowania w konwersjach do TXT.
Ten przewodnik pomaga zrozumieć kod; samodzielne wyjaśnienie na obronie jest
obowiązkiem osoby oddającej projekt. Użycie AI ujawniono w README.
