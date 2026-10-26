# Minimalne dowody konwersji

Wejścia znajdują się w `../examples/`. Zachowano po jednym wyniku każdej grupy
oraz oba PDF, aby można było obejrzeć rezultat bez uruchamiania aplikacji.

| Plik | Wejście i konwersja | Oczekiwany wynik |
|---|---|---|
| dane.json | examples/dane.csv → JSON (grupa A) | Kolejność kolumn, polskie znaki i puste pole bez zmian |
| tekst.docx | examples/tekst.txt → DOCX (grupa B) | Linie jako akapity, polskie znaki, pusty akapit |
| tekst.odt | examples/tekst.txt → ODT (grupa B) | Te same akapity, spacje i tabulatory |
| z-docx.pdf | tekst.docx → PDF (grupa C) | Czytelny tekst z polskimi znakami |
| z-odt.pdf | tekst.odt → PDF (grupa C) | Czytelny tekst z polskimi znakami |

Wyniki wygenerowano 26.10.2026. Konwersje odwrotne CSV i TXT sprawdzają testy;
usunięto ich kopie identyczne z przykładami. Odczyt PDF przez pdftotext potwierdził
polskie znaki. Szczegóły i ograniczenia: `../docs/RAPORT_TESTOW.md`.
