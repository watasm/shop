from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from cart.models import Cart

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders', null=True)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField()
    address = models.CharField(max_length = 250)
    postal_code = models.CharField(max_length = 20)
    city = models.CharField(max_length = 100)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    paid = models.BooleanField(default = False)
    braintree_id = models.CharField(max_length=150, blank=True)
    #coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    # def get_discount(self):
    #     total_cost = self.get_total_cost_before_discount()
    #     return total_cost * (self.discount / Decimal('100'))


    def get_discount(self, coupon):
        discount = Decimal('0')
        items = self.items.all()
        discounted_items = items.filter(product__seller=coupon.seller)
        discount += coupon.discount / Decimal('100') * sum(i.get_cost() for i in discounted_items)
        discount = round(discount,2)
        return discount


    def get_sum_discount(self):
        discount = Decimal('0')
        coupons = self.coupons.only('seller', 'discount')
        items = self.items.all()
        for coupon in coupons:
            discounted_items = items.filter(product__seller=coupon.seller)
            discount += coupon.discount / Decimal('100') * sum(i.get_cost() for i in discounted_items)
        return discount


    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        discount = self.get_sum_discount()
        return total_cost - discount

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name = 'items', on_delete = models.CASCADE)
    product = models.ForeignKey(Product, related_name = 'order_items', on_delete = models.CASCADE)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    quantity = models.PositiveIntegerField(default = 1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
