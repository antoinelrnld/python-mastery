# validate.py
class Validator:
    def __init__(self, name=None):
        self.name = name
    
    def __set_name__(self, cls, name):
        self.name = name
    
    @classmethod
    def check(cls, value):
        return value
    
    def __set__(self, instance, value):
        instance.__dict__[self.name] = self.check(value)

class Typed(Validator):
    expected_type = object
    @classmethod
    def check(cls, value):
        if not isinstance(value, cls.expected_type):
            raise TypeError(f'Expected {cls.expected_type}')
        return super().check(value)

class Integer(Typed):
    expected_type = int

class Float(Typed):
    expected_type = float

class String(Typed):
    expected_type = str


class Positive(Validator):
    @classmethod
    def check(cls, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        return super().check(value)

class NonEmpty(Validator):
    @classmethod
    def check(cls, value):
        if len(value) == 0:
            raise ValueError('Must be non-empty')
        return super().check(value)

class PositiveInteger(Integer, Positive):
    pass

class PositiveFloat(Float, Positive):
    pass

class NonEmptyString(String, NonEmpty):
    pass



from inspect import signature
class ValidatedFunction:
    def __init__(self, func):
        self.func = func
        self.signature = signature(func)

    def __call__(self, *args, **kwargs):
        print('Calling', self.func)
        bound = self.signature.bind(*args, **kwargs)
        for name, val in dict(self.func.__annotations__).items():
            val.check(bound.arguments[name])
        result = self.func(*args, **kwargs)
        return result


from functools import wraps
def validated(func):
    sig = signature(func)
    
    annotations = dict(func.__annotations__)
    
    return_check = annotations.pop('return', None)
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Calling', func.__name__)
        bound = sig.bind(*args, **kwargs)

        errors = []
        for name, val in annotations.items():
            try:
                val.check(bound.arguments[name])
            except Exception:
                errors.append(f'{name}: Expected {val.expected_type}')
        if errors:
            raise TypeError('Bad Arguments\n' + '\n'.join(errors))

        result = func(*args, **kwargs)
        if return_check:
            try:
                return_check.check(result)
            except Exception:
                raise TypeError(f'Bad return : Expected {sig.return_annotation.expected_type}')
        return result
    return wrapper


def enforce(**annotations):
    return_check = annotations.pop('return_', None)
    
    def decorate(func):
        sig = signature(func)
    
        @wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            errors = []
            
            for name, val in annotations.items():
                try:
                    val.check(bound.arguments[name])
                except Exception:
                    errors.append(f'{name}: Expected {val.expected_type}')
            if errors:
                raise TypeError('Bad Arguments\n' + '\n'.join(errors))

            result = func(*args, **kwargs)
            if return_check:
                try:
                    return_check.check(result)
                except Exception:
                    raise TypeError(f'Bad return : Expected {sig.return_annotation.expected_type}')
            return result
        return wrapper
    return decorate


class Stock:
    name = String()
    shares = PositiveInteger()
    price = PositiveFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self._shares = shares
        self._price = price

    @property
    def cost(self):
        return self._shares * self._price

    @validated
    def sell(self, nshares: PositiveInteger):
        if nshares > self._shares:
            raise ValueError
        self._shares -= nshares

    def __repr__(self):
        return f'Stock(\'{self.name}\', {self._shares}, {self._price})'