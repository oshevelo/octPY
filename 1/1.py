
def parce_price(price):
    try:
        return float(price)
    except:
        return 0
            

def calc_total_price(discount, price, vat=0.2):
    print('vat={}'.format(vat))
    price = price + price * vat
    if discount == 0:
        return price

    return price * discount


price = input('enter price :')
z = calc_total_price(price=parce_price(price), discount=0)
print(z)
