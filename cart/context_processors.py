from .cart import Cart
from .models import Cart as CartModel
from django.shortcuts import get_object_or_404

def cart(request):
    if request.user.is_authenticated and not request.user.is_superuser and not hasattr(request.user, 'seller'):
        cart = get_object_or_404(CartModel, user=request.user)
        return {'cart': cart}

    return {'cart': Cart(request)}
