from collections.abc import Sequence
from collections import namedtuple
import csv

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



class RideData(Sequence):
    def __init__(self):
        # Each value is a list with all the values (a column)
        self.routes = []
        self.dates = []
        self.daytypes = []
        self.numrides = []
        
    def __len__(self):
        # All lists assumed to have the same length
        return len(self.routes)

    def __getitem__(self, index):
        if type(index) is slice:
            return [{ 'route': self.routes[i],
                    'date': self.dates[i],
                    'daytype': self.daytypes[i],
                    'rides': self.numrides[i]
                    } for i in range(index.start, index.stop, index.step or 1)]
        return { 'route': self.routes[index],
                 'date': self.dates[index],
                 'daytype': self.daytypes[index],
                 'rides': self.numrides[index] }

    def append(self, d):
        self.routes.append(d['route'])
        self.dates.append(d['date'])
        self.daytypes.append(d['daytype'])
        self.numrides.append(d['rides'])


def read_rides_as_data_structure(filename, data_structure):
    '''
    Read the bus ride data as a list of given data_structure
    '''
    records = RideData()
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
    data_structure = 'dict'
    rows = read_rides_as_data_structure('../../../Data/ctabus.csv', data_structure)
    print(data_structure)
    print('Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())
