from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Seller
from .forms import SellerForm
from accounts.forms import UserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.db.models.signals import post_save
from .tasks import send_verification_email
# Create your views here.


@receiver(post_save, sender = Seller)
def seller_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        # Send verification email
        send_verification_email.delay(instance.pk)


def seller_registration(request):
    seller_form = SellerForm()
    user_form = UserForm()
    if request.method == 'POST':
        seller_form = SellerForm(request.POST)
        user_form = UserForm(request.POST)
        if seller_form.is_valid() and user_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_seller = seller_form.save(commit = False)
            new_seller.user = new_user
            new_seller.save()

            login(request, authenticate(
                username = user_form.cleaned_data['username'],
                password = user_form.cleaned_data['password']
            ))
            return redirect('shop:product_list')
    return render(request, 'sellers/registration.html', {'seller_form': seller_form, 'user_form': user_form})

@login_required(login_url='accounts/login/')
def profile(request, id):
    user = get_object_or_404(User, id=id)

    context = {
        'user': user,
    }
    return render(request, 'sellers/profile.html', context)


def email_check(request):
    if request.is_ajax():
        email = request.POST.get('email')
        if User.objects.filter(email=email):
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'ko'})
