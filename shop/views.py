from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from shop.models import Category, Product, ProductRating
from cart.forms import CartAddProductForm
from .recommender import Recommender
from .forms import ProductAddForm, ProductEditForm
from sellers.models import Seller
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from django.contrib.auth.decorators import login_required

from .forms import ProductReviewForm

def product_list(request, category_slug = None):
    categories = Category.objects.all()
    products = Product.objects.filter(available = True)

    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        products = products.filter(category = category)
    else:
        category = None

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }

    return render(request, 'shop/product/list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id = id, slug = slug, available = True)
    cart_add_product_form = CartAddProductForm()
    product_review_form = ProductReviewForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    if request.method=='POST' and request.user.is_authenticated:
        review = ProductReviewForm(request.POST)

        if review.is_valid():
            new_review = review.save(commit=False)
            new_review.user = request.user
            new_review.product = product
            new_review.save()
            return redirect(product.get_absolute_url())

    context = {
        'product': product,
        'cart_add_product_form': cart_add_product_form,
        'recommended_products': recommended_products,
        'product_review_form': product_review_form
    }

    return render(request, 'shop/product/detail.html', context)

@login_required
def add_product(request):
    product_form = ProductAddForm()
    is_seller = False
    if request.user.is_authenticated and request.user.seller:
        is_seller = True
        if request.method == "POST":
            product_form = ProductAddForm(request.POST, request.FILES)
            if product_form.is_valid():
                new_product = product_form.save(commit=False)
                new_product.slug = slugify(new_product.name)
                new_product.seller = request.user.seller
                new_product.save()
                return redirect(reverse('shop:product_detail', args=[new_product.id, new_product.slug]))

    else:
        return HttpResponse("<h1>You are not seller</h1>", status=403)

    return render(request, 'shop/product/add_product.html', {'product_form': product_form, 'is_seller': is_seller})

@login_required(login_url='accounts/login/')
def edit_product(request, id, slug):
    product=get_object_or_404(Product, id=id, slug=slug)
    if request.user.is_authenticated:
        if request.user != product.seller.user and not request.user.is_superuser:
            raise PermissionDenied
        if request.method=='POST':
            product_edit_form = ProductEditForm(instance=product, data=request.POST, files=request.FILES)

            if product_edit_form.is_valid():
                product_edit_form.save()

            return redirect(reverse('shop:product_detail', args=[product.id, product.slug]))
        else:
            product_edit_form = ProductEditForm(instance=product)

    return render(request, 'shop/product/edit_product.html', {'product_edit_form': product_edit_form})

@login_required(login_url='accounts/login/')
def delete_product(request, id, slug):
    product=get_object_or_404(Product, id=id, slug=slug)
    if request.user.is_authenticated:
        if request.user != product.seller.user and not request.user.is_superuser:
            raise PermissionDenied
        product.delete()
        return redirect('shop:product_list')

@login_required
def update_avg(request):
    if request.is_ajax():
        product = get_object_or_404(Product, id=request.POST.get('id'))
        rating = request.POST.get('rating')
        if ProductRating.objects.filter(user=request.user, product=product).exists():
            obj = ProductRating.objects.get(user=request.user, product=product)
            obj.rating = rating
            obj.save(update_fields=['rating'])
            product.rating_average = product.rating.all().aggregate(Avg('rating'))['rating__avg']
            product.save(update_fields=['rating_average'])

        else:
            ProductRating.objects.create(user=request.user, product=product, rating=rating)

        return JsonResponse({'total_rating': product.rating_average})

    return HttpResponse('Bad request', status=400)
