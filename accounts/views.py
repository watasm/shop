from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import UserForm, ProfilesForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from sellers.models import Seller
from .models import Profiles
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models.signals import post_save, m2m_changed
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.tasks import send_verification_email
from cart.models import Cart



@receiver(post_save, sender = Profiles)
def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        # Send verification email
        send_verification_email.delay(instance.pk)


def signup(request):
    user_form = UserForm()
    profiles_form = ProfilesForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profiles_form = ProfilesForm(request.POST, request.FILES)

        if user_form.is_valid() and profiles_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            Cart.objects.create(user=new_user)
            new_profiles = profiles_form.save(commit = False)
            new_profiles.user = new_user
            new_profiles.save()
            profiles_form.save_m2m()

            login(request, authenticate(
                username = user_form.cleaned_data['username'],
                password = user_form.cleaned_data['password']
            ))

            return redirect('shop:product_list')

    return render(request, 'allauth/account/signup.html', {'user_form': user_form, 'profiles_form': profiles_form,})

def verify(request, uuid):
    if hasattr(request.user, 'seller'):
        try:
            seller = Seller.objects.get(verification_uuid=uuid, is_verified=False)
        except Profiles.DoesNotExist:
            return HttpResponse("User does not exist or is already verified", status=404)

        seller.is_verified = True
        seller.save()

    else:
        try:
            profile = Profiles.objects.get(verification_uuid=uuid, is_verified=False)
        except Profiles.DoesNotExist:
            return HttpResponse("User does not exist or is already verified", status=404)

        profile.is_verified = True
        profile.save()

    return redirect('shop:product_list')


@login_required(login_url='accounts/login/')
def profile(request, id):
    user = get_object_or_404(User, id=id)
    is_seller=False
    try:
        if user.seller:
            is_seller = True
    except Seller.DoesNotExist:
        pass


    #object_list = Article.objects.filter(user=user)
    #paginator = Paginator(object_list, 2)
    #page = request.GET.get('page')
    #try:
        #articles = paginator.page(page)
    #except PageNotAnInteger:
        #articles = paginator.page(1)
    #except EmptyPage:
        #articles = paginator.page(paginator.num_pages)


    context = {
        'user': user,
        'is_seller':is_seller,
        #'articles': articles,
    }
    return render(request, 'shop/profile.html', context)


@login_required(login_url='accounts/login/')
def userEdit(request):
    user=request.user
    if request.method=='POST':
        try:
            profile_form = ProfileUpdateForm(instance=user.profiles, data=request.POST, files=request.FILES)
        except ObjectDoesNotExist:
            profile_form = ProfileUpdateForm(data=request.POST, files=request.FILES)
            new_profile = profile_form.save(commit = False)
            new_profile.user = user
            new_profile.save()
        user_form = UserUpdateForm(instance=user, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return redirect('shop:product_list')
    else:
        try:
            profile_form = ProfileUpdateForm(instance=user.profiles)
        except ObjectDoesNotExist:
            profile_form = ProfileUpdateForm()
        user_form = UserUpdateForm(instance=user)


    return render(request, 'shop/useredit.html', {'user':user_form, 'profile':profile_form})

def email_check(request):
    if request.is_ajax():
        email = request.POST.get('email')
        if User.objects.filter(email=email):
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'ko'})
