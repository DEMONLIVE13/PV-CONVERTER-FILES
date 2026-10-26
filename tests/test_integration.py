"""Regresje etapu końcowego i testy integracyjne zależności systemowych."""
import builtins
import logging
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from converter.core import ConversionError, execute, validate

logging.getLogger('converter.core').addHandler(logging.NullHandler())


class FinalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / 'tekst.txt'
        self.source.write_text('Zażółć gęślą jaźń.\n\nŁódź  i\tKraków\n', encoding='utf-8')

    def test_validate_and_empty_choices(self):
        self.assertEqual(validate(self.source, 'ODT', self.root), (self.source, '.odt', self.root))
        for args in [('', 'odt', self.root), (self.source, '', self.root), (self.source, 'odt', '')]:
            with self.subTest(args=args), self.assertRaises(ConversionError):
                validate(*args)

    def test_write_permission_failure_leaves_no_result(self):
        with patch('converter.core.tempfile.TemporaryDirectory', side_effect=PermissionError('odmowa')):
            with self.assertRaisesRegex(ConversionError, 'uprawnień'):
                execute(self.source, 'odt', self.root)
        self.assertEqual(list(self.root.iterdir()), [self.source])

    def test_missing_docx_library(self):
        original = builtins.__import__
        def import_without_docx(name, *args, **kwargs):
            if name == 'docx':
                raise ImportError('symulowany brak biblioteki')
            return original(name, *args, **kwargs)
        with patch('builtins.__import__', side_effect=import_without_docx):
            with self.assertRaisesRegex(ConversionError, 'pip install'):
                execute(self.source, 'docx', self.root)

    def test_corrupt_office_input_never_starts_process(self):
        for suffix in ['.docx', '.odt']:
            source = self.root / ('uszkodzony' + suffix)
            source.write_text('to nie jest dokument ZIP', encoding='utf-8')
            with patch('converter.core.find_libreoffice', return_value='soffice'), patch('converter.core.subprocess.run') as run:
                with self.assertRaisesRegex(ConversionError, 'Uszkodzony'):
                    execute(source, 'pdf', self.root)
                run.assert_not_called()

    def test_office_start_failure(self):
        source = execute(self.source, 'odt', self.root)
        with patch('converter.core.find_libreoffice', return_value='soffice'), patch('converter.core.subprocess.run', side_effect=OSError('odmowa')):
            with self.assertRaisesRegex(ConversionError, 'uruchomić LibreOffice'):
                execute(source, 'pdf', self.root)

    def test_error_is_logged(self):
        with self.assertLogs('converter.core', level='ERROR') as captured:
            with self.assertRaises(ConversionError):
                execute(self.source, 'json', self.root)
        self.assertIn('Nieobsługiwana', '\n'.join(captured.output))

    def test_cli_bad_json(self):
        source = self.root / 'bad.json'
        source.write_text('{', encoding='utf-8')
        result = subprocess.run([sys.executable, '-m', 'converter', str(source), 'csv', '-o', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('linia 1', result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertFalse((self.root / 'bad.csv').exists())

    def test_real_office_pdf(self):
        from converter.core import find_libreoffice
        try:
            find_libreoffice()
        except ConversionError as error:
            self.skipTest(str(error))
        for suffix in ['docx', 'odt']:
            with self.subTest(suffix=suffix):
                document = execute(self.source, suffix, self.root)
                pdf = execute(document, 'pdf', self.root)
                self.assertTrue(pdf.read_bytes().startswith(b'%PDF-'))
                if shutil.which('pdftotext'):
                    result = subprocess.run(['pdftotext', str(pdf), '-'], capture_output=True, text=True, check=True)
                    self.assertIn('Zażółć gęślą jaźń.', result.stdout)


class GuiTests(unittest.TestCase):
    def setUp(self):
        import tkinter as tk
        try:
            self.window = tk.Tk()
        except tk.TclError as error:
            self.skipTest(f'Brak ekranu: {error}')
        self.addCleanup(self.window.destroy)
        self.window.withdraw()
        from converter.gui import ConverterApp
        self.app = ConverterApp(self.window)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_dynamic_formats_and_busy_state(self):
        source = self.root / 'a.csv'
        source.write_text('imię\nŁukasz\n', encoding='utf-8')
        self.app.source.set(str(source))
        self.app.output.set(str(self.root))
        self.assertEqual(tuple(self.app.formats['values']), ('.json',))
        self.assertEqual(str(self.app.convert_button['state']), 'normal')
        self.app.set_busy(True)
        self.assertEqual(str(self.app.convert_button['state']), 'disabled')
        self.assertEqual(str(self.app.source_entry['state']), 'disabled')
        self.app.set_busy(False)
        self.app.source.set(str(self.root / 'a.xyz'))
        self.assertEqual(tuple(self.app.formats['values']), ())
        self.assertEqual(str(self.app.convert_button['state']), 'disabled')

    def test_worker_result_and_safe_names(self):
        source = self.root / 'a.csv'
        source.write_text('imię\nŁukasz\n', encoding='utf-8')
        from converter.gui import messagebox
        with patch.object(messagebox, 'showinfo') as info:
            for expected in ['a.json', 'a_1.json']:
                self.app.worker(str(source), 'json', str(self.root))
                self.app.poll_result()
                self.assertTrue((self.root / expected).is_file())
            self.assertEqual(info.call_count, 2)
        with patch.object(messagebox, 'showerror') as error:
            self.app.worker(str(source), 'pdf', str(self.root))
            self.app.poll_result()
            error.assert_called_once()
