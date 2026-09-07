# readrides.py

import csv
from collections import namedtuple


NamedTupleRow = namedtuple('Row', ['route', 'date', 'daytype', 'rides'])


class ClassRow:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


class SlotsClassRow:
    __slots__ = ['route', 'date', 'daytype', 'rides']
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


def read_rides_as_data_structure(filename, data_structure):
    '''
    Read the bus ride data as a list of given data_structure
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            match data_structure:
                case 'tuple':
                    record = (route, date, daytype, rides)
                case 'dict':
                    record = {
                        'route': route,
                        'date': date,
                        'daytype': daytype,
                        'rides': rides
                    }
                case 'class':
                    record = ClassRow(route, date, daytype, rides)
                case 'named_tuple':
                    record = NamedTupleRow(route, date, daytype, rides)
                case 'slots_class':
                    record = SlotsClassRow(route, date, daytype, rides)
            records.append(record)
    return records


if __name__ == '__main__':
    import tracemalloc
    tracemalloc.start()
    data_structure = 'slots_class'
    rows = read_rides_as_data_structure('../../../Data/ctabus.csv', data_structure)
    print(data_structure)
    print('Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())
