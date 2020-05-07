from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart as CartModel, CartItem

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def on_login(sender, user, request, **kwargs):
    try:
        session_cart = request.session['cart']
        cart = get_object_or_404(CartModel, user=user)

        for key in session_cart:    # key is product id
            product = get_object_or_404(Product, id=key)
            if CartItem.objects.filter(product=product, cart=cart).exists():
                item = CartItem.objects.get(product=product, cart=cart)
                item.quantity = session_cart[str(key)]['quantity']
                item.save(update_fields=['quantity'])

            else:
                CartItem.objects.create(cart=cart, product=product, price=product.price, quantity=session_cart[str(key)]['quantity'])
    except:
        print('Error when adding products to cart.')



def cart_detail(request):

    if request.user.is_authenticated:
        coupon_apply_form = CouponApplyForm()
        cart = get_object_or_404(CartModel, user=request.user)
        return render(request, 'cart/detail_for_users.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})
    else:
        cart = Cart(request)
        return render(request, 'cart/detail.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    form = CartAddProductForm(request.POST)
    if request.user.is_authenticated:
        cart = get_object_or_404(CartModel, user=request.user)
    else:
        cart = Cart(request)

    if form.is_valid():
        cd = form.cleaned_data
        item = cart.get_item(product_id)
        if item:
            quantity = item.quantity if (request.user.is_authenticated) else item['quantity']

        if ((not item or cd['update']) and (product.quantity >=cd['quantity'])) or (item and product.quantity >= cd['quantity']+quantity):
            cart.add(product = product, quantity = cd['quantity'], update_quantity = cd['update'])
            return redirect('cart:cart_detail')

        messages.error(request, 'Add error. There is no so much {} in the store. There is only left {} item.'.format(product.name, product.quantity))
        return redirect(product.get_absolute_url())
    else:
        return HttpResponse('Bad request', status=400)


def cart_remove(request, product_id):
    if request.user.is_authenticated:
        cart = get_object_or_404(CartModel, user=request.user)
    else:
        cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart:cart_detail')
