from structure import Structure
import inspect


class Stock(Structure):
    def __init__(self, name, shares, price):
        self._init()
    
    @classmethod
    def set_fields(cls):
        cls._fields = tuple(inspect.signature(Stock).parameters)

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares

Stock.set_fields()