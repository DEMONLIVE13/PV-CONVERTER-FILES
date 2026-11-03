# Zachowane wyniki konwersji

Pliki pochodzą z dostarczonego archiwum. Pozostawiono ich oryginalne nazwy.
Wejścia demonstracyjne znajdują się w ../examples/. Raport i ograniczenia
weryfikacji znajdują się w ../RAPORT_TESTOW.md.

| Pliki | Co sprawdzić |
|---|---|
| dane.json, dane_1.json | Wyniki CSV -> JSON; lista obiektów, polskie znaki, puste pole i kolejność kluczy. Oba pliki zawierają te same dane. |
| dane.csv | Wynik JSON -> CSV; nagłówki oraz pola zgodne z przykładem. |
| tekst.docx, tekst.odt | Wyniki konwersji tekstu do dokumentów; polskie znaki i podział na akapity. |
| tekst.txt, tekst_1.txt | Wyniki zwrotne do tekstu; porównaj treść z examples/tekst.txt. |
| tekst.pdf, tekst_1.pdf | Zachowane PDF-y z dokumentów; sprawdź otwieranie i widoczną treść. |

Przyrostek _1 wynika z ochrony istniejącej nazwy. Sama nazwa nie identyfikuje
kierunku konwersji. Kierunek nowych prób ustalaj na podstawie pliku wejściowego
lub zapisuj wyniki w osobnych katalogach.
