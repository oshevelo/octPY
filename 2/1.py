
class Device:

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_sell_price(self, discount, vat=0.2):

        price = self.price + self.price * vat
        if discount == 0:
            return price

        return price * discount

class Monitor(Device):
    def __str__(self):
        return 'monitor {}'.format(self.name)


class Notebook(Device):
    def __str__(self):
        return 'Notebook {}'.format(self.name)


class Cart:
    products = []

    def add_product(self, product):
        self.products.append(product)


n = Notebook(name = 'apple', price = 100)
m = Monitor(name = 'samsung', price = 100)
print(n)
c = Cart()

c.add_product(n)
c.add_product(m)

print([str(p) for p in c.products])
print(c.products[0].get_sell_price(0))
print(c.products[0])
