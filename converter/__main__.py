import argparse
import sys
from .core import ConversionError, REGISTRY, execute


def main():
    parser = argparse.ArgumentParser(description='Uniwersalny konwerter — lab. 2–3')
    parser.add_argument('source', nargs='?', help='Plik wejściowy')
    parser.add_argument('format', nargs='?', help='Format docelowy, np. json')
    parser.add_argument('-o', '--output-dir', default='.', help='Istniejący katalog docelowy')
    parser.add_argument('--list', action='store_true', help='Lista wspieranych par')
    args = parser.parse_args()
    if args.list:
        for source, target in sorted(REGISTRY):
            print(f'{source} → {target}')
        return 0
    if not args.source or not args.format:
        parser.error('Podaj plik wejściowy i format docelowy.')
    try:
        print(f'Zapisano: {execute(args.source, args.format, args.output_dir)}')
        return 0
    except ConversionError as error:
        print(f'Błąd: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
