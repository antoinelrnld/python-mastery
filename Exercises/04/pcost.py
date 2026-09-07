def portfolio_cost(filename: str):
    total = 0
    with open(filename) as f:
        while line := f.readline():
            _, nshare, price = line.split()
            try:
                total += int(nshare) * float(price)
            except ValueError as e:
                print(f'Couldn\'t parse: {line}', end='')
                print(f'Reason: {e}')
    return total

if __name__ == '__main__':
    print(portfolio_cost('../../Data/portfolio3.dat'))
    