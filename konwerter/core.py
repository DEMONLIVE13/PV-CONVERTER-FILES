"""Walidacja, rejestr konwerterów i bezpieczny zapis wyników."""

from dataclasses import dataclass
from pathlib import Path
from collections.abc import Callable
import csv
import io
import json


class ConversionError(Exception):
    """Błąd, który można przedstawić użytkownikowi bez tracebacka."""


REGISTRY: dict[tuple[str, str], Callable[[Path], str]] = {}


def converter(source: str, target: str):
    def register(function):
        REGISTRY[(source, target)] = function
        return function
    return register


def available_targets(source: Path) -> list[str]:
    return sorted(target for src, target in REGISTRY if src == source.suffix.lower())


@dataclass(frozen=True)
class ConversionRequest:
    source: Path
    target_format: str
    output_dir: Path

    @property
    def normalized_target(self) -> str:
        return "." + self.target_format.lower().lstrip(".")

    def validate(self) -> None:
        if not self.source.is_file():
            raise ConversionError("Nie znaleziono pliku wejściowego. Sprawdź ścieżkę.")
        if not self.output_dir.is_dir():
            raise ConversionError("Katalog wynikowy nie istnieje. Utwórz go przed konwersją.")
        if (self.source.suffix.lower(), self.normalized_target) not in REGISTRY:
            raise ConversionError("Nieobsługiwana para formatów. Użyj opcji --lista.")


@converter(".csv", ".json")
def csv_to_json(source: Path) -> str:
    with source.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file, strict=True)
        columns = next(reader, None)
        if not columns or any(not name.strip() for name in columns):
            raise ConversionError("CSV musi zawierać niepusty wiersz nagłówków i niepuste nazwy kolumn.")
        if len(set(columns)) != len(columns):
            raise ConversionError("Nazwy kolumn CSV nie mogą się powtarzać.")
        records = []
        for row in reader:
            if len(row) != len(columns):
                raise ConversionError(f"CSV: rekord kończący się w linii {reader.line_num} ma inną liczbę pól niż nagłówek.")
            records.append(dict(zip(columns, row)))
    if not records:
        raise ConversionError("CSV musi zawierać co najmniej jeden rekord, aby zachować nagłówki w JSON.")
    return json.dumps(records, ensure_ascii=False, indent=2) + "\n"


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ConversionError(f"JSON zawiera powtórzony klucz: {key}.")
        result[key] = value
    return result


def invalid_constant(value):
    raise ConversionError(f"JSON zawiera niedozwoloną wartość {value}.")


@converter(".json", ".csv")
def json_to_csv(source: Path) -> str:
    try:
        data = json.loads(source.read_text(encoding="utf-8-sig"),
                          object_pairs_hook=unique_object, parse_constant=invalid_constant)
    except json.JSONDecodeError as error:
        raise ConversionError(f"Błędny JSON: linia {error.lineno}, kolumna {error.colno}. Popraw składnię pliku.") from error
    if not isinstance(data, list) or not data or not all(isinstance(row, dict) for row in data):
        raise ConversionError("JSON musi być niepustą listą obiektów (rekordów).")
    columns = list(data[0])
    if not columns or any(not name.strip() for name in columns):
        raise ConversionError("JSON musi zawierać niepuste nazwy kolumn.")
    for number, row in enumerate(data, start=1):
        if set(row) != set(columns):
            raise ConversionError(f"Rekord JSON {number} ma inne kolumny niż pierwszy rekord.")
        if any(not isinstance(value, str) for value in row.values()):
            raise ConversionError(f"Rekord JSON {number}: wszystkie wartości muszą być tekstem; pustą wartość zapisz jako \"\".")
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows(data)
    return buffer.getvalue()


def execute(request: ConversionRequest) -> Path:
    try:
        request.validate()
        content = REGISTRY[(request.source.suffix.lower(), request.normalized_target)](request.source)
        # Tryb x gwarantuje brak nadpisania również przy równoczesnym zapisie.
        for number in range(10000):
            suffix = "" if number == 0 else f"_{number}"
            target = request.output_dir / f"{request.source.stem}{suffix}{request.normalized_target}"
            try:
                file = target.open("x", encoding="utf-8", newline="")
            except FileExistsError:
                continue
            try:
                with file:
                    file.write(content)
            except OSError:
                target.unlink(missing_ok=True)
                raise
            return target
        raise ConversionError("Brak wolnej nazwy wyniku. Wybierz inny katalog.")
    except UnicodeError as error:
        raise ConversionError("Niepoprawne kodowanie. Zapisz plik wejściowy jako UTF-8.") from error
    except csv.Error as error:
        raise ConversionError(f"Błędny CSV: {error}. Sprawdź cudzysłowy i separator przecinek.") from error
    except OSError as error:
        raise ConversionError(f"Błąd odczytu lub zapisu: {error.strerror}. Sprawdź uprawnienia i ścieżki.") from error
