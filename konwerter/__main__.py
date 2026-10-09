"""Uruchomienie: python -m konwerter plik.csv --format json --katalog wyniki."""

import argparse
from pathlib import Path
import sys

from .core import ConversionError, ConversionRequest, REGISTRY, execute


def main() -> int:
    parser = argparse.ArgumentParser(description="Konwerter CSV ↔ JSON — laboratorium 2")
    parser.add_argument("plik", nargs="?", type=Path, help="ścieżka pliku wejściowego")
    parser.add_argument("--format", help="format docelowy: csv lub json")
    parser.add_argument("--katalog", type=Path, help="istniejący katalog wynikowy")
    parser.add_argument("--lista", action="store_true", help="pokaż działające kierunki konwersji")
    args = parser.parse_args()
    if args.lista:
        for source, target in sorted(REGISTRY):
            print(f"{source[1:].upper()} → {target[1:].upper()}")
        return 0
    if args.plik is None or not args.format or args.katalog is None:
        parser.error("podaj plik, --format i --katalog albo użyj --lista")
    try:
        target = execute(ConversionRequest(args.plik, args.format, args.katalog))
    except ConversionError as error:
        print(f"Błąd: {error}", file=sys.stderr)
        return 1
    print(f"Gotowe. Zapisano: {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
