import sys

class Structure:

    @staticmethod
    def _init():
        locs  = sys._getframe(1).f_locals
        self = locs['self']
        for name, val in locs.items():
            if name == 'self': continue
            setattr(self, name, val)
    
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
