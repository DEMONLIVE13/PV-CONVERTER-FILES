import argparse
import logging
from pathlib import Path
import tempfile
import sys
from .core import ConversionError, REGISTRY, execute


def main():
    parser = argparse.ArgumentParser(description='Uniwersalny konwerter plików')
    parser.add_argument('source', nargs='?', help='Plik wejściowy')
    parser.add_argument('format', nargs='?', help='Format docelowy, np. json')
    parser.add_argument('-o', '--output-dir', default='.', help='Istniejący katalog docelowy')
    parser.add_argument('--gui', action='store_true', help='Uruchom interfejs graficzny')
    parser.add_argument('--list', action='store_true', help='Lista wspieranych par')
    args = parser.parse_args()
    log_path = Path(tempfile.gettempdir()) / 'pv-converter.log'
    try:
        logging.basicConfig(filename=log_path, encoding='utf-8', level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    except OSError:
        logging.basicConfig(level=logging.INFO)
    if args.gui or len(sys.argv) == 1:
        try:
            from .gui import main as gui_main
        except ImportError:
            print('Brak Tkinter. Windows: zmodyfikuj instalację Pythona i włącz Tcl/Tk. Linux: zainstaluj python3-tk.', file=sys.stderr)
            return 1
        try:
            gui_main()
        except Exception as error:
            from tkinter import TclError
            if not isinstance(error, TclError):
                raise
            print('Nie można uruchomić okna. Sprawdź środowisko graficzne i instalację Tcl/Tk. '
                  'Możesz użyć CLI: python -m converter --help', file=sys.stderr)
            return 1
        return 0
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
