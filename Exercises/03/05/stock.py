class Stock:
    __slots__ = ['name', '_shares', '_price']
    
    _types = (str, int, float)
    def __init__(self, name, shares, price):
        self.name = name
        self._shares = shares
        self._price = price

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)

    @property
    def cost(self):
        return self._shares * self._price

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        expected_type = self._types[self.__slots__.index('_share')]
        if type(value) is not expected_type:
            raise TypeError(f"Expected {expected_type.__name__}")
        if value < 0:
            raise ValueError("shares must be >= 0")
        self._shares = value

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        expected_type = self._types[self.__slots__.index('_price')]
        if type(value) is not expected_type:
            raise TypeError(f"Expected {expected_type.__name__}")
        if value < 0:
            raise ValueError("price must be >= 0")
        self._price = value

    def sell(self, nshares):
        if nshares > self._shares:
            raise ValueError
        self._shares -= nshares
 

def print_portfolio(portfolio: list[Stock]):
    print('%10s %10s %10s' % ('name', 'shares', 'price'))
    print('---------- ' * 3)
    for s in portfolio:
        print('%10s %10d %10.2f' % (s.name, s._shares, s._price))
