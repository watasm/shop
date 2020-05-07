from django.db import models
from shop.models import Product
from django.contrib.auth.models import User
from decimal import Decimal
import time

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return 'Cart id {}. User {}.'.format(self.id, self.user)

    def __len__(self):
        return sum(item.quantity for item in self.items.all())

    def add(self, product, quantity = 1, update_quantity = False):
        item = self.get_item(product.id)
        if not item:
            CartItem.objects.create(cart=self, product=product, price=product.price, quantity=quantity)

        else:
            if update_quantity:
                item.quantity = quantity
            else:
                item.quantity += quantity

            item.save(update_fields=['quantity'])

    def remove(self, product_id):
        if self.items.filter(product__id = product_id):
            self.items.get(product__id = product_id).delete()

    def get_item(self, product_id):
        if self.items.filter(product__id = product_id):
            return self.items.get(product__id = product_id)
        return False

    def get_total_price(self):
        return sum(item.get_price() for item in self.items.all())

    def get_sum_discount(self):
        discount = Decimal('0')
        coupons = self.coupons.only('seller', 'discount')
        items = self.items.all()
        for coupon in coupons:
            discounted_items = items.filter(product__seller=coupon.seller)
            discount += coupon.discount / Decimal('100') * sum(i.get_price() for i in discounted_items)
        return discount

    def get_discount(self, coupon):
        discount = Decimal('0')
        items = self.items.all()
        discounted_items = items.filter(product__seller=coupon.seller)
        discount += coupon.discount / Decimal('100') * sum(i.get_price() for i in discounted_items)

        discount = round(discount,2)
        return discount

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_sum_discount()

    def clear(self):
        self.items.all().delete()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name = 'items', on_delete = models.CASCADE)
    product = models.ForeignKey(Product, related_name = 'cart_items', on_delete = models.CASCADE)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    quantity = models.PositiveIntegerField(default = 1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_price(self):
        return self.price * self.quantity
