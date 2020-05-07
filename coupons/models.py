from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from sellers.models import Seller
from cart.models import Cart
from orders.models import Order

# class Coupon(models.Model):
#     code = models.CharField(max_length=50, unique=True)
#     valid_from = models.DateTimeField()
#     valid_to = models.DateTimeField()
#     discount = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(100)])
#     active = models.BooleanField()
#
#     def __str__(self):
#         return self.code


class SellerCoupon(models.Model):
    code = models.CharField(max_length=10, unique=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='coupons')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupons', null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='coupons', null=True, blank=True)
    discount = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(100)])
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='coupons', null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
