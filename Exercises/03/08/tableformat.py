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


def create_formatter(format, upper_headers = False, columns_formats=None):
    if format == 'html':
        cls = HTMLTableFormatter
    if format == 'csv':
        cls = CSVTableFormatter
    if format == 'text':
        cls = TextTableFormatter
    if upper_headers:
        class cls(UpperHeadersMixin, cls):
            pass
    if columns_formats:
        class cls(ColumnFormatMixin, cls):
            formats = columns_formats
    return cls()
    


def print_table(records: list[object], fields: list[str], formatter: TableFormatter):
    if not issubclass(formatter, TableFormatter):
        raise TypeError("Expected a TableFormatter")
    formatter.headings(fields)
    for r in records:
        rowdata = [getattr(r, fieldname) for fieldname in fields]
        formatter.row(rowdata)


class ColumnFormatMixin:
    formats = []
    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)


class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])
