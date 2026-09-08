import csv

class Stock:
    types = (str, int, float)
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls.types, row)]
        return cls(*values)

    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        if nshares > self.shares:
            raise ValueError
        self.shares -= nshares
 

def print_portfolio(portfolio: list[Stock]):
    print('%10s %10s %10s' % ('name', 'shares', 'price'))
    print('---------- ' * 3)
    for s in portfolio:
        print('%10s %10d %10.2f' % (s.name, s.shares, s.price))
