# reader.py

import csv
from typing import Iterable

def read_csv_as_dicts(filename: str, types: list[type], headers: list[str]=None) -> list[dict]:
    '''
    Read CSV data into a list of dictionaries with optional type conversion
    '''
    with open(filename) as file:
        return csv_as_dicts(file, types, headers)

def read_csv_as_instances(filename: str, cls: type, headers: list[str]=None):
    '''
    Read CSV data into a list of instances
    '''
    with open(filename) as file:
        return csv_as_instances(file, cls, headers)


def csv_as_dicts(lines: Iterable, types: list[type], headers: list[str]=None):
    records = []
    rows = csv.reader(lines)
    headers = headers or next(rows)
    for row in rows:
        record = { name: func(val) 
                    for name, func, val in zip(headers, types, row) }
        records.append(record)
    return records


def csv_as_instances(lines: Iterable, cls: type, headers: list[str]=None):
    records = []
    rows = csv.reader(lines)
    headers = headers or next(rows)
    for row in rows:
        record = cls.from_row(row)
        records.append(record)
    return records
