import csv
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile
import xml.etree.ElementTree as ET


class ConversionError(Exception):
    """Błąd, który można bezpiecznie pokazać użytkownikowi."""


REGISTRY = {}


def converter(source, target):
    def register(function):
        REGISTRY[(source, target)] = function
        return function
    return register


def available_targets(source):
    return sorted(target for src, target in REGISTRY if src == Path(source).suffix.lower())


@converter('.csv', '.json')
def csv_to_json(source, target):
    with source.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames
        if not headers or any(not h for h in headers) or len(set(headers)) != len(headers):
            raise ConversionError('CSV musi mieć niepuste, unikalne nagłówki.')
        rows = list(reader)
        if any(None in row or None in row.values() for row in rows):
            raise ConversionError('Liczba pól CSV nie odpowiada nagłówkom.')
        if not rows:
            raise ConversionError('CSV musi zawierać przynajmniej jeden rekord, aby zachować nagłówki w JSON.')
    target.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')


@converter('.json', '.csv')
def json_to_csv(source, target):
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ConversionError('JSON zawiera powtórzony klucz.')
            result[key] = value
        return result
    rows = json.loads(source.read_text(encoding='utf-8-sig'), object_pairs_hook=unique_object)
    if not isinstance(rows, list) or not rows or any(not isinstance(row, dict) or not row for row in rows):
        raise ConversionError('JSON musi być niepustą listą niepustych obiektów.')
    headers = list(rows[0])
    if any(not h for h in headers):
        raise ConversionError('Nazwy kolumn nie mogą być puste.')
    if any(set(row) != set(headers) for row in rows):
        raise ConversionError('Wszystkie rekordy JSON muszą mieć te same klucze.')
    if any(not isinstance(value, str) for row in rows for value in row.values()):
        raise ConversionError('Wartości JSON muszą być tekstem; puste pole zapisuj jako "".')
    with target.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def docx_library():
    try:
        from docx import Document
        return Document
    except ImportError as error:
        raise ConversionError('Brak python-docx. Uruchom: python -m pip install -r requirements.txt') from error


@converter('.txt', '.docx')
def txt_to_docx(source, target):
    document = docx_library()()
    for line in source.read_text(encoding='utf-8-sig').split('\n'):
        document.add_paragraph(line)
    document.save(target)


@converter('.docx', '.txt')
def docx_to_txt(source, target):
    document = docx_library()(source)
    target.write_text('\n'.join(p.text for p in document.paragraphs), encoding='utf-8')


OFFICE = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'
TEXT = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'


@converter('.txt', '.odt')
def txt_to_odt(source, target):
    root = ET.Element(f'{{{OFFICE}}}document-content', {f'{{{OFFICE}}}version': '1.2'})
    body = ET.SubElement(root, f'{{{OFFICE}}}body')
    text = ET.SubElement(body, f'{{{OFFICE}}}text')
    for line in source.read_text(encoding='utf-8-sig').split('\n'):
        paragraph = ET.SubElement(text, f'{{{TEXT}}}p')
        # Preserve repeated spaces and tabs using ODF text elements.
        for character in line:
            if character in (' ', '\t'):
                ET.SubElement(paragraph, f'{{{TEXT}}}' + ('s' if character == ' ' else 'tab'))
            elif len(paragraph):
                paragraph[-1].tail = (paragraph[-1].tail or '') + character
            else:
                paragraph.text = (paragraph.text or '') + character
    manifest = ('<?xml version="1.0" encoding="UTF-8"?>'
                '<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">'
                '<manifest:file-entry manifest:full-path="/" manifest:media-type="application/vnd.oasis.opendocument.text"/>'
                '<manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>'
                '</manifest:manifest>')
    with zipfile.ZipFile(target, 'w') as archive:
        archive.writestr('mimetype', 'application/vnd.oasis.opendocument.text', compress_type=zipfile.ZIP_STORED)
        archive.writestr('content.xml', ET.tostring(root, encoding='utf-8', xml_declaration=True))
        archive.writestr('META-INF/manifest.xml', manifest)


@converter('.odt', '.txt')
def odt_to_txt(source, target):
    def content(node):
        value = node.text or ''
        for child in node:
            if child.tag == f'{{{TEXT}}}s':
                count = int(child.get(f'{{{TEXT}}}c', '1'))
                if not 1 <= count <= 100000:
                    raise ConversionError('Nieprawidłowa liczba spacji w ODT.')
                value += ' ' * count
            elif child.tag == f'{{{TEXT}}}tab':
                value += '\t'
            elif child.tag == f'{{{TEXT}}}line-break':
                value += '\n'
            else:
                value += content(child)
            value += child.tail or ''
        return value
    with zipfile.ZipFile(source) as archive:
        root = ET.fromstring(archive.read('content.xml'))
    body = root.find(f'{{{OFFICE}}}body/{{{OFFICE}}}text')
    if body is None:
        raise ConversionError('ODT nie zawiera dokumentu tekstowego.')
    paragraphs = [content(node) for node in body.iter() if node.tag in (f'{{{TEXT}}}p', f'{{{TEXT}}}h')]
    target.write_text('\n'.join(paragraphs), encoding='utf-8')


def find_libreoffice():
    configured = os.environ.get('LIBREOFFICE_PATH')
    candidates = [configured] if configured else [
        'libreoffice', 'soffice', '/Applications/LibreOffice.app/Contents/MacOS/soffice',
        r'C:\Program Files\LibreOffice\program\soffice.exe',
        r'C:\Program Files (x86)\LibreOffice\program\soffice.exe']
    for candidate in candidates:
        executable = shutil.which(candidate)
        if executable:
            return executable
    raise ConversionError('Nie znaleziono LibreOffice. Zainstaluj pakiet lub ustaw LIBREOFFICE_PATH na plik wykonywalny soffice.')


@converter('.docx', '.pdf')
@converter('.odt', '.pdf')
def office_to_pdf(source, target):
    executable = find_libreoffice()
    with tempfile.TemporaryDirectory() as directory:
        work = Path(directory)
        result = subprocess.run([
            executable, f'-env:UserInstallation={(work / "profile").as_uri()}',
            '--headless', '--convert-to', 'pdf', '--outdir', str(work), str(source.resolve())
        ], capture_output=True, text=True, timeout=60, shell=False)
        if result.returncode != 0:
            raise ConversionError(f'LibreOffice zakończył się kodem {result.returncode}: {result.stderr.strip() or result.stdout.strip()}')
        pdf = work / (source.stem + '.pdf')
        if not pdf.is_file() or pdf.stat().st_size == 0 or not pdf.read_bytes().startswith(b'%PDF-'):
            raise ConversionError('LibreOffice nie utworzył poprawnego pliku PDF.')
        shutil.copyfile(pdf, target)


def execute(source, target_format, output_dir):
    source, output_dir = Path(source), Path(output_dir)
    target_format = '.' + target_format.lower().lstrip('.')
    if not source.is_file():
        raise ConversionError('Nie znaleziono pliku wejściowego.')
    if not output_dir.is_dir():
        raise ConversionError('Katalog docelowy nie istnieje.')
    function = REGISTRY.get((source.suffix.lower(), target_format))
    if function is None:
        raise ConversionError('Nieobsługiwana para formatów.')
    # Konwersja do pliku tymczasowego; finalny plik tworzony wyłącznie bez nadpisania.
    try:
        with tempfile.TemporaryDirectory(dir=output_dir) as directory:
            temporary = Path(directory) / ('result' + target_format)
            function(source, temporary)
            index = 0
            while True:
                suffix = f'_{index}' if index else ''
                target = output_dir / (source.stem + suffix + target_format)
                try:
                    destination = target.open('xb')
                    break
                except FileExistsError:
                    index += 1
            try:
                with destination, temporary.open('rb') as stream:
                    shutil.copyfileobj(stream, destination)
            except Exception:
                target.unlink(missing_ok=True)
                raise
            return target
    except ConversionError:
        raise
    except subprocess.TimeoutExpired as error:
        raise ConversionError('LibreOffice przekroczył limit 60 sekund.') from error
    except Exception as error:
        raise ConversionError(f'Konwersja nie powiodła się: {error}') from error
