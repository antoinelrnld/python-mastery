from abc import ABC, abstractmethod

class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers):
        raise NotImplementedError()

    @abstractmethod
    def row(self, rowdata):
        raise NotImplementedError()


class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        print(' '.join('%10s' % h for h in headers))
        print(('-'*10 + ' ')*len(headers))
    
    def row(self, rowdata):
        print(' '.join('%10s' % d for d in rowdata))


class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        print(','.join(headers))
    
    def row(self, rowdata):
        print(','.join([str(rd) for rd in rowdata]))


class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        print('<tr> ' + ' '.join([f'<th>{header}</th>' for header in headers]) + ' </tr>')
    
    def row(self, rowdata):
        print('<tr> ' + ' '.join([f'<td>{rd}</td>' for rd in rowdata]) + ' </tr>')


def create_formatter(format):
    if format == 'html':
        return HTMLTableFormatter()
    if format == 'csv':
        return CSVTableFormatter()
    if format == 'text':
        return TextTableFormatter()


def print_table(records: list[object], fields: list[str], formatter: TableFormatter):
    if not issubclass(formatter, TableFormatter):
        raise TypeError("Expected a TableFormatter")
    formatter.headings(fields)
    for r in records:
        rowdata = [getattr(r, fieldname) for fieldname in fields]
        formatter.row(rowdata)
