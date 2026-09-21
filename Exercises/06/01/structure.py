class Structure:
    def __init__(self, *args):
        attrs = getattr(self, '_fields')
        if len(args) != len(attrs):
            raise TypeError(f'Expected {len(attrs)} arguments')
        for attr, arg in zip(attrs, args):
            setattr(self, attr, arg)
    
    def __repr__(self):
        return f'{self.__class__.__name__}{tuple(getattr(self, attr) for attr in self._fields)}'
    
    def __setattr__(self, name: str, value):
        if name not in self._fields and not name.startswith('_'):
            raise AttributeError(f'No attribute {name}')
        self.__dict__[name] = value


class Stock(Structure):
    _fields = ('name', 'shares', 'price')

class Date(Structure):
    _fields = ('year', 'month', 'day')
