from django.shortcuts import render, reverse, redirect, get_object_or_404
from .models import Order, OrderItem
from .forms import OrderCreateForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .tasks import order_created
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from shop.recommender import Recommender


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})

@login_required
def order_create(request):
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            cart = get_object_or_404(Cart, user=request.user)
            coupons = cart.coupons.only('order')
            order = form.save(commit=False)
            order.cart = cart
            order.save()
            for coupon in coupons:
                coupon.order = order
                coupon.save(update_fields=['order'])


            temp = []
            r = Recommender()

            for item in cart.items.all():
                OrderItem.objects.create(order=order, product=item.product, price=item.price, quantity=item.quantity)
                temp.append(item.product)

            r.products_bought(temp)
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))

    else:
        form = OrderCreateForm()

    return render(request, 'orders/order/create_for_users.html', {'form': form})
