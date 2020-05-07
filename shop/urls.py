from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name = 'product_list'),
    path('<slug:category_slug>/', views.product_list, name = 'product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name = 'product_detail'),
    path('add_product', views.add_product, name = 'add_product'),
    path('edit_product/<int:id>/<slug:slug>/', views.edit_product, name = 'edit_product'),
    path('delete_product/<int:id>/<slug:slug>/', views.delete_product, name = 'delete_product'),
    path('update_average', views.update_avg, name='update_average'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
