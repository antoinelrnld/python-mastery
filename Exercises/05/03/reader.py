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
    return convert_csv(lines, lambda headers, row: { name: func(val) for name, func, val in zip(headers, types, row) }, headers)


def csv_as_instances(lines: Iterable, cls: type, headers: list[str]=None):
    return convert_csv(lines, lambda _, row: cls.from_row(row), headers)



def make_dict(headers, row):
        return dict(zip(headers, row))

def convert_csv(lines, func, headers=None):
    rows = csv.reader(lines)
    headers = headers or next(rows)
    return list(map(lambda row: func(headers, row), rows))
