import csv
import json
from pathlib import Path
import tempfile
import unittest

from konwerter.core import ConversionError, ConversionRequest, available_targets, execute


class ConverterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def source(self, name, content):
        path = self.root / name
        path.write_text(content, encoding='utf-8')
        return path

    def convert(self, source, target):
        return execute(ConversionRequest(source, target, self.root))

    def test_round_trip_polish_empty_quotes_and_multiline(self):
        content = 'imię,kod,uwagi\nŁukasz,0012,"kawa, herbata"\nZośka,,"dwa\nakapity"\n'
        source = self.source('osoby.csv', content)
        intermediate = self.convert(source, 'json')
        data = json.loads(intermediate.read_text(encoding='utf-8'))
        self.assertEqual(list(data[0]), ['imię', 'kod', 'uwagi'])
        self.assertEqual(data[0]['kod'], '0012')
        self.assertEqual(data[1]['kod'], '')
        result = self.convert(intermediate, 'csv')
        with source.open(encoding='utf-8', newline='') as left, result.open(encoding='utf-8', newline='') as right:
            self.assertEqual(list(csv.reader(left)), list(csv.reader(right)))

    def test_json_key_order_comes_from_first_record(self):
        source = self.source('a.json', '[{"b":"ż","a":""},{"a":"x","b":"y"}]')
        self.assertEqual(self.convert(source, 'csv').read_text(encoding='utf-8'), 'b,a\nż,\ny,x\n')

    def test_invalid_json_reports_location(self):
        source = self.source('a.json', '[{"x":}]')
        with self.assertRaisesRegex(ConversionError, 'linia 1, kolumna'):
            self.convert(source, 'csv')
        self.assertFalse((self.root / 'a.csv').exists())

    def test_invalid_json_structures(self):
        for content in ['[]', '{}', '[1]', '[{}]', '[{"x":null}]', '[{"x":1}]', '[{"x":"a"},{"y":"b"}]', '[{"x":"a","x":"b"}]', '[{"x":NaN}]']:
            with self.subTest(content=content):
                source = self.source('a.json', content)
                with self.assertRaises(ConversionError):
                    self.convert(source, 'csv')

    def test_invalid_csv(self):
        for content in ['', 'x\n', 'x,x\na,b\n', ',y\na,b\n', 'x,y\na\n', 'x\n"unfinished']:
            with self.subTest(content=content):
                source = self.source('a.csv', content)
                with self.assertRaises(ConversionError):
                    self.convert(source, 'json')

    def test_bom_and_uppercase_extension(self):
        source = self.source('a.CSV', '\ufeffimię\nŁukasz\n')
        self.assertEqual(json.loads(self.convert(source, '.JSON').read_text(encoding='utf-8')), [{'imię': 'Łukasz'}])

    def test_existing_result_is_preserved(self):
        source = self.source('a.csv', 'x\na\n')
        old = self.source('a.json', 'oryginał')
        self.assertEqual(self.convert(source, 'json').name, 'a_1.json')
        self.assertEqual(old.read_text(encoding='utf-8'), 'oryginał')

    def test_missing_file_directory_and_unsupported_pair(self):
        source = self.source('a.csv', 'x\na\n')
        requests = [ConversionRequest(self.root / 'missing.csv', 'json', self.root),
                    ConversionRequest(source, 'json', self.root / 'missing'),
                    ConversionRequest(source, 'pdf', self.root)]
        for request in requests:
            with self.subTest(request=request), self.assertRaises(ConversionError):
                execute(request)

    def test_available_targets(self):
        self.assertEqual(available_targets(Path('a.CSV')), ['.json'])
        self.assertEqual(available_targets(Path('a.json')), ['.csv'])
        self.assertEqual(available_targets(Path('a.txt')), [])

    def test_invalid_encoding(self):
        source = self.root / 'a.csv'
        source.write_bytes(b'x\n\xff\n')
        with self.assertRaisesRegex(ConversionError, 'UTF-8'):
            self.convert(source, 'json')


if __name__ == '__main__':
    unittest.main()
