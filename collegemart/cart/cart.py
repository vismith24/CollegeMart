from decimal import Decimal
from django.conf import settings
from seller.models import Products_Selling as Product
from seller.models import Products_Leasing


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, rec, quantity=1, update_quantity=False):
        if rec == 0:
            product_id = 'S' + str(product.id)
        else:
            product_id = 'L' + str(product.id)
        if product_id not in self.cart:
            if rec == 0:
                self.cart[product_id] = {'quantity': 0, 'price': str(product.price), 'rec': str(rec), 'prod_id': str(product.id)}
            else:
                self.cart[product_id] = {'quantity': 0, 'price': str(product.price1), 'rec': str(rec), 'prod_id': str(product.id)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product, rec):
        if rec == 0:
            product_id = 'S' + str(product.id)
        else:
            product_id = 'L' + str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        selling_ids = [int(v['prod_id']) for k,v in self.cart.items() if v['rec'] == '0']
        leasing_ids = [int(v['prod_id']) for k,v in self.cart.items() if v['rec'] == '1']
        product_ids = self.cart.keys()
        products_selling = Product.objects.filter(id__in=selling_ids)
        products_leasing = Products_Leasing.objects.filter(id__in=leasing_ids)
        for product in products_selling:
            self.cart['S'+str(product.id)]['sproduct'] = product
        for product in products_leasing:
            self.cart['L'+str(product.id)]['lproduct'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True