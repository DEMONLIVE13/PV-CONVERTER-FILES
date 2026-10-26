from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from converter.core import ConversionError, execute

class DocumentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
    def file(self, name, text):
        p = self.root / name
        p.write_text(text, encoding='utf-8')
        return p
    def test_docx(self):
        p = self.file('a.txt', 'Zażółć gęślą jaźń.\n\nAkapit.\n')
        self.assertEqual(execute(execute(p,'docx',self.root),'txt',self.root).read_text(encoding='utf-8'), p.read_text(encoding='utf-8'))
    def test_odt(self):
        p = self.file('a.txt', 'Łódź  i\tKraków\n\nAkapit.\n')
        self.assertEqual(execute(execute(p,'odt',self.root),'txt',self.root).read_text(encoding='utf-8'), p.read_text(encoding='utf-8'))
    @patch.dict('os.environ', {'LIBREOFFICE_PATH':'/missing/soffice'})
    def test_missing_office(self):
        with self.assertRaisesRegex(ConversionError,'Nie znaleziono LibreOffice'):
            execute(self.file('a.odt','test'),'pdf',self.root)
    @patch('converter.core.find_libreoffice', return_value='soffice')
    @patch('converter.core.subprocess.run')
    def test_process(self, run, find):
        p = execute(self.file('a.txt', 'Zażółć'), 'odt', self.root)
        run.return_value = subprocess.CompletedProcess([],7,'','awaria')
        with self.assertRaisesRegex(ConversionError,'kodem 7'): execute(p,'pdf',self.root)
        self.assertFalse(run.call_args.kwargs['shell'])
        run.return_value = subprocess.CompletedProcess([],0,'','')
        with self.assertRaisesRegex(ConversionError,'nie utworzył'): execute(p,'pdf',self.root)
        run.side_effect = subprocess.TimeoutExpired('soffice',60)
        with self.assertRaisesRegex(ConversionError,'60 sekund'): execute(p,'pdf',self.root)
