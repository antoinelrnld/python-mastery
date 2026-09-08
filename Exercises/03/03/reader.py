import csv
from collections.abc import Sequence

def read_csv_as_dicts(filepath: str, conversions: list[type]):
    with open(filepath) as f:
        csv_reader = csv.reader(f)
        headers = next(csv_reader) 
        return [{name: func(val) for name, func, val in zip(headers, conversions, row)} for row in csv_reader]


class DataCollection(Sequence):
    def __init__(self, headers):
        # Each value is a list with all the values (a column)
        self.headers = headers
        for header in headers:
            self.__setattr__(header, [])
        
    def __len__(self):
        # All lists assumed to have the same length
        return len(self.__getattribute__(self.headers[0]))
        
    def __getitem__(self, index):
        if type(index) is slice:
            return [{ h: self.__getattribute__(h)[i] for h in self.headers
                    } for i in range(index.start, index.stop, index.step or 1)]
        return { h: self.__getattribute__(h)[index] for h in self.headers }

    def append(self, d):
        for k in d:
            self.__getattribute__(k).append(d[k])

def read_csv_as_columns(filepath: str, conversions: list[type]):
    with open(filepath) as f:
        csv_reader = csv.reader(f)
        headers = next(csv_reader)
        data = DataCollection(headers)
        for row in csv_reader:
            data.append({name: func(val) for name, func, val in zip(headers, conversions, row)})
        return data

def read_csv_as_instances(filename, cls):
    '''
    Read a CSV file into a list of instances
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            records.append(cls.from_row(row))
    return records