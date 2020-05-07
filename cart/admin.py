from django.contrib import admin
from .models import Cart, CartItem
from coupons.models import SellerCoupon

class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']

class SellerCouponInline(admin.TabularInline):
    model = SellerCoupon

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline, SellerCouponInline]
