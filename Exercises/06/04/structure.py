class Structure:

    @classmethod
    def create_init(cls):
        argstr = ','.join(cls._fields)
        code = f'def __init__(self, {argstr}):\n'
        for name in cls._fields:
            code += f'    self.{name} = {name}\n'
        locs = {}
        exec(code, locs)
        cls.__init__ = locs['__init__']
    
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
