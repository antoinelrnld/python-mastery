# structure.py
from validate import Validator
from collections import ChainMap


class StructureMeta(type):
    @classmethod
    def __prepare__(meta, clsname, bases):
        return ChainMap({}, Validator.validators)
        
    @staticmethod
    def __new__(meta, name, bases, methods):
        methods = methods.maps[0]
        return super().__new__(meta, name, bases, methods)


class Structure(metaclass=StructureMeta):
    _fields = ()
    _types = ()

    def __setattr__(self, name, value):
        if name.startswith('_') or name in self._fields:
            super().__setattr__(name, value)
        else:
            raise AttributeError('No attribute %s' % name)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__,
                           ', '.join(repr(getattr(self, name)) for name in self._fields))

    @classmethod
    def create_init(cls):
        '''
        Create an __init__ method from _fields
        '''
        args = ','.join(cls._fields)
        code = f'def __init__(self, {args}):\n'
        for name in cls._fields:
            code += f'    self.{name} = {name}\n'
        locs = { }
        exec(code, locs)
        cls.__init__ = locs['__init__']
    
    @classmethod
    def __init_subclass__(cls):
        validate_attributes(cls)
        
    @classmethod
    def from_row(cls, row):
        rowdata = [func(val) for func, val in zip(cls._types, row)]
        return cls(*rowdata)


def validate_attributes(cls):
    validators = []
    for _, val in vars(cls).items():
        if isinstance(val, Validator):
            validators.append(val)
    cls._fields = [val.name for val in validators]
    cls._types = [val.expected_type for val in validators if val.expected_type]
    if isinstance(cls, Structure):
        cls.create_init()
    return cls


def typed_structure(clsname, **validators):
    cls = type(clsname, (Structure,), validators)
    return cls