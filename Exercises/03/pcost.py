def compute_price():
    total = 0
    with open('../../Data/portfolio.dat') as f:
        while line := f.readline():
            _, nshare, price = line.split()
            total += int(nshare) * float(price)
    return total

if __name__ == '__main__':
    price = compute_price()
    print(price)
    