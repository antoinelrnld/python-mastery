# readrides.py

import csv
from collections import namedtuple, Counter, defaultdict

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
    data_structure = 'dict'
    rows = read_rides_as_data_structure('../../../Data/ctabus.csv', data_structure)
    
    # Q1.
    routes = set()
    for row in rows:
        routes.add(row['route'])
        
    # Q2.
    n_on_date = {}
    for row in rows:
        n_on_date[row['route'], row['date']] = row['rides']

    # Q3.
    total_per_route = Counter()
    for row in rows:
        total_per_route[row['route']] += row['rides']
    
    # Q4.
    data2001 = [row for row in rows if row['date'][-4:] == '2001']
    data2011 = [row for row in rows if row['date'][-4:] == '2011']
    count2001 = Counter()
    count2011 = Counter()
    for row in data2001:
        count2001[row['route']] += row['rides']
    for row in data2011:
        count2011[row['route']] += row['rides']
        
        
    # Q4.
    count_by_year = defaultdict(Counter)
    for row in rows:
        year = row['date'][-4:]
        count_by_year[year][row['route']] += row['rides']
    

    print(f'1. How many bus routes exist in Chicago? Answer: {len(routes)}')
    print(f'2. How many people rode the number 22 bus on February 2, 2011? What about any route on any date of your choosing? Answer: {n_on_date['22', '02/02/2011']}')
    print(f'3. What is the total number of rides taken on each bus route? Answer: {total_per_route.most_common(3)}')
    print(f'4. What five bus routes had the greatest ten-year increase in ridership from 2001 to 2011? Answer: {(count_by_year['2011'] - count_by_year['2001']).most_common(5)}')
