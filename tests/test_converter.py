import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from converter.core import ConversionError, execute, available_targets

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
    def file(self, name, text):
        p = self.root / name
        p.write_text(text, encoding='utf-8')
        return p
    def test_csv_json(self):
        p = self.file('a.csv', 'imię,uwagi\nŁukasz,\nŻaneta,"a,b"\n')
        j = execute(p, 'json', self.root)
        self.assertEqual(json.loads(j.read_text(encoding='utf-8'))[0], {'imię':'Łukasz','uwagi':''})
        c = execute(j, 'csv', self.root)
        self.assertEqual(c.name, 'a_1.csv')
        self.assertEqual(json.loads(execute(c, 'json', self.root).read_text(encoding='utf-8')), json.loads(j.read_text(encoding='utf-8')))
    def test_invalid_json(self):
        for text in ['{', '[{"a":"1"},{"b":"2"}]', '[{"a":null}]', '[{"a":"1","a":"2"}]']:
            with self.assertRaises(ConversionError):
                execute(self.file('bad.json', text), 'csv', self.root)
    def test_invalid_csv(self):
        for text in ['a,a\n1,2\n', 'a,b\n1\n', 'a,b\n']:
            with self.assertRaises(ConversionError):
                execute(self.file('bad.csv', text), 'json', self.root)
    def test_docx(self):
        p = self.file('a.txt', 'Zażółć gęślą jaźń.\n\nAkapit.\n')
        self.assertEqual(execute(execute(p,'docx',self.root),'txt',self.root).read_text(encoding='utf-8'), p.read_text(encoding='utf-8'))
    def test_odt(self):
        p = self.file('a.txt', 'Łódź  i\tKraków\n\nAkapit.\n')
        self.assertEqual(execute(execute(p,'odt',self.root),'txt',self.root).read_text(encoding='utf-8'), p.read_text(encoding='utf-8'))
    def test_validation(self):
        p = self.file('a.TXT', 'tekst')
        self.assertEqual(available_targets(p), ['.docx','.odt'])
        for src, fmt, out in [(self.root/'missing','docx',self.root),(p,'json',self.root),(p,'odt',self.root/'missing')]:
            with self.assertRaises(ConversionError): execute(src,fmt,out)
    @patch.dict('os.environ', {'LIBREOFFICE_PATH':'/missing/soffice'})
    def test_missing_office(self):
        with self.assertRaisesRegex(ConversionError,'Nie znaleziono LibreOffice'):
            execute(self.file('a.odt','test'),'pdf',self.root)
    def valid_odt(self):
        return execute(self.file('a.txt', 'Zażółć gęślą jaźń.'), 'odt', self.root)

    @patch('converter.core.find_libreoffice', return_value='soffice')
    @patch('converter.core.subprocess.run')
    def test_process_nonzero_exit(self, run, find):
        p = self.valid_odt()
        run.return_value = subprocess.CompletedProcess([], 7, '', 'awaria')
        with self.assertRaisesRegex(ConversionError, 'kodem 7'):
            execute(p, 'pdf', self.root)
        self.assertFalse(run.call_args.kwargs['shell'])
        self.assertEqual(run.call_args.kwargs['timeout'], 60)
        self.assertFalse((self.root / 'a.pdf').exists())

    @patch('converter.core.find_libreoffice', return_value='soffice')
    @patch('converter.core.subprocess.run')
    def test_process_missing_pdf(self, run, find):
        p = self.valid_odt()
        run.return_value = subprocess.CompletedProcess([], 0, '', '')
        with self.assertRaisesRegex(ConversionError, 'nie utworzył'):
            execute(p, 'pdf', self.root)

    @patch('converter.core.find_libreoffice', return_value='soffice')
    @patch('converter.core.subprocess.run', side_effect=subprocess.TimeoutExpired('soffice', 60))
    def test_process_timeout(self, run, find):
        p = self.valid_odt()
        with self.assertRaisesRegex(ConversionError, '60 sekund'):
            execute(p, 'pdf', self.root)

    @patch('converter.core.find_libreoffice', return_value='soffice')
    @patch('converter.core.subprocess.run')
    def test_damaged_office_does_not_start_process(self, run, find):
        with self.assertRaisesRegex(ConversionError, 'Uszkodzony DOCX/ODT'):
            execute(self.file('a.odt', 'test'), 'pdf', self.root)
        run.assert_not_called()

    @patch('converter.core.tempfile.TemporaryDirectory', side_effect=PermissionError('denied'))
    def test_write_permission_message(self, temporary):
        with self.assertRaisesRegex(ConversionError, 'Brak uprawnień'):
            execute(self.file('a.csv', 'x\na\n'), 'json', self.root)

    def test_log_contains_error(self):
        import logging
        from converter.core import _LOGGER
        log_path = self.root / 'test.log'
        handler = logging.FileHandler(log_path, encoding='utf-8')
        _LOGGER.addHandler(handler)
        try:
            with self.assertRaises(ConversionError):
                execute(self.root / 'missing.csv', 'json', self.root)
            handler.flush()
            self.assertIn('Nie znaleziono pliku wejściowego', log_path.read_text(encoding='utf-8'))
        finally:
            _LOGGER.removeHandler(handler)
            handler.close()
