"""Odtwarzalne próby T1–T8. Wymaga LibreOffice oraz pdftotext (Poppler)."""
import csv
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
from docx import Document

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dowody_lab3'
OUT.mkdir(exist_ok=True)
if any(OUT.iterdir()):
    raise SystemExit('Katalog dowody_lab3 musi być pusty. Przenieś poprzednie dowody przed ponowieniem.')
log = []


def run(source, fmt, *, missing=False, expected=0):
    args = [sys.executable, '-m', 'converter', str(source), fmt, '-o', str(OUT)]
    env = os.environ.copy()
    if missing:
        env['LIBREOFFICE_PATH'] = str(OUT / 'nieistniejacy-soffice')
    result = subprocess.run(args, cwd=ROOT, env=env, capture_output=True,
                            text=True, encoding='utf-8', errors='replace', timeout=90, shell=False)
    log.append(f'$ {shlex.join(args)}\nKod CLI: {result.returncode}\n{result.stdout}{result.stderr}')
    assert result.returncode == expected, log[-1]
    return result


run(ROOT / 'examples/dane.csv', 'json')
assert json.loads((OUT/'dane.json').read_text(encoding='utf-8')) == json.loads((ROOT/'examples/dane.json').read_text(encoding='utf-8'))
run(ROOT / 'examples/dane.json', 'csv')
with (ROOT/'examples/dane.csv').open(encoding='utf-8', newline='') as a, (OUT/'dane.csv').open(encoding='utf-8', newline='') as b:
    assert list(csv.reader(a)) == list(csv.reader(b))
run(ROOT / 'examples/tekst.txt', 'docx')
text = (ROOT/'examples/tekst.txt').read_text(encoding='utf-8')
assert [p.text for p in Document(OUT/'tekst.docx').paragraphs] == text.split('\n')
run(OUT/'tekst.docx', 'pdf')
assert (OUT/'tekst.pdf').read_bytes().startswith(b'%PDF-')
pdf_text = subprocess.run(['pdftotext', str(OUT/'tekst.pdf'), '-'], capture_output=True,
                          text=True, encoding='utf-8', check=True, timeout=30, shell=False).stdout
assert ' '.join(text.split()) == ' '.join(pdf_text.split())
(OUT/'tekst_pdf_odczyt.txt').write_text(pdf_text, encoding='utf-8')
run(OUT/'tekst.docx', 'pdf', missing=True, expected=1)
broken = OUT/'uszkodzony.docx'
broken.write_text('To nie jest dokument DOCX.', encoding='utf-8')
run(broken, 'pdf', expected=1)
assert not (OUT/'uszkodzony.pdf').exists()
original = (OUT/'tekst.pdf').read_bytes()
run(OUT/'tekst.docx', 'pdf')
assert (OUT/'tekst.pdf').read_bytes() == original
assert (OUT/'tekst_1.pdf').read_bytes().startswith(b'%PDF-')
spaced = OUT/'dokument ze spacjami.docx'
spaced.write_bytes((OUT/'tekst.docx').read_bytes())
run(spaced, 'pdf')
assert (OUT/'dokument ze spacjami.pdf').read_bytes().startswith(b'%PDF-')
(OUT/'przebieg.txt').write_text('\n'.join(log), encoding='utf-8')
print('T1–T8: OK. Dowody: dowody_lab3/')
