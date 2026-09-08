import csv

class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        if nshares > self.shares:
            raise ValueError
        self.shares -= nshares


def read_portfolio(filepath: str):
    stocks = []
    with open(filepath) as f:
        reader = csv.reader(f)
        _ = next(reader)
        for name, shares, price in reader:
            stocks.append(Stock(name, int(shares), float(price)))
    return stocks   

def print_portfolio(portfolio: list[Stock]):
    print('%10s %10s %10s' % ('name', 'shares', 'price'))
    print('---------- ' * 3)
    for s in portfolio:
        print('%10s %10d %10.2f' % (s.name, s.shares, s.price))
