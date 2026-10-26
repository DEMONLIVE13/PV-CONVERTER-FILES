# Zgodność z instrukcją projektu

Podstawa: załączony PDF „Projekt 1. Uniwersalny konwerter plików”.
Stan po weryfikacji 26.10.2026.

| Wymaganie | Realizacja |
|---|---|
| Grupa A: CSV↔JSON | 2 kierunki, walidacja i udokumentowana semantyka |
| Grupa B: minimum 2 | 4 kierunki: TXT↔DOCX oraz TXT↔ODT |
| Grupa C: minimum 2 | DOCX→PDF i ODT→PDF przez LibreOffice |
| GUI Tkinter/ttk | Wybór pliku/katalogu/formatu, status, komunikaty i blokada przycisku |
| Responsywność | Wątek roboczy, Queue, odbiór wyniku przez root.after |
| Walidacja | Plik, katalog, rozszerzenie, para, puste wybory, zależność i zapis |
| Konflikty nazw | Ekskluzywne tworzenie xb i przyrostki _1, _2 itd. |
| Jakość | UTF-8, polskie znaki, kolejność kolumn, puste pola i akapity |
| Architektura | core.py oddzielony od gui.py; rejestr dekoratorów, validate i execute |
| Proces zewnętrzny | Lista argumentów, shell=False, limit czasu, osobny profil, kontrola kodu i wyniku |
| Logowanie | Przyczyna i traceback błędu, czas operacji; konfiguracja logu w CLI/GUI |
| Testy | 28 przechodzących testów; aktualny raport oraz pliki dowodowe |
| Dokumentacja | README, requirements, macierz par i ograniczeń, źródła, ujawnienie AI |
| Przykłady | CSV, JSON, TXT i błędny JSON z opisem oczekiwań |
| Dziennik prac | Oryginalny CHANGELOG oraz rzeczywisty wpis końcowej weryfikacji |

Nie przypisano punktów za terminowość, obronę ani samodzielność.
Te elementy wymagają oceny prowadzącej. Wcześniejsze daty w CHANGELOG pochodzą
z dostarczonego archiwum i nie zostały niezależnie potwierdzone.
Autor wpisany w README pochodzi z projektu wejściowego.
