from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import SellerCoupon
from .forms import CouponApplyForm
from cart.models import Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# @require_POST
# def coupon_apply(request):
#     now = timezone.now()
#     form = CouponApplyForm(request.POST)
#     if form.is_valid():
#         code = form.cleaned_data['code']
#         try:
#             coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
#             request.session['coupon_id'] = coupon.id
#         except Coupon.DoesNotExist:
#             request.session['coupon_id'] = None
#     return redirect('cart:cart_detail')

@require_POST
@login_required
def seller_coupon_apply(request):
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        cart = get_object_or_404(Cart, user=request.user)
        try:
            coupon = SellerCoupon.objects.get(code__iexact=code, active=True)
            if cart.items.filter(product__seller=coupon.seller):
                coupon.cart = cart
                coupon.save(update_fields=['user', 'cart'])
                messages.success(request, 'Coupon succsessfuly added')
                return redirect('cart:cart_detail')
            else:
                messages.error(request, 'No match')
                return redirect('cart:cart_detail')
        except:
            messages.error(request, 'Coupon not found or has already been used.')

    return redirect('cart:cart_detail')

@require_POST
@login_required
def seller_coupon_detach(request, id):
    coupon = get_object_or_404(SellerCoupon, id=id)
    if request.user == coupon.user and coupon.cart != None:
        coupon.cart = None
        coupon.save(update_fields=['cart'])
        messages.success(request, 'Coupon succsessfuly detached')
    else:
        messages.error(request, 'Error when detaching coupon.')
    return redirect('cart:cart_detail')
