from django.db import models
from django.shortcuts import reverse
from sellers.models import Seller
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from datetime import datetime

class Category(models.Model):
    name = models.CharField(max_length = 200, db_index = True)
    slug = models.SlugField(max_length = 200, unique = True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    seller=models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, related_name = 'products', on_delete = models.CASCADE)
    name = models.CharField(max_length = 200, db_index = True)
    slug = models.SlugField(max_length = 200, db_index = True)
    image = models.ImageField(upload_to = 'products/%Y/%m/%d', blank = True)
    description = models.TextField(blank = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    available = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    quantity = models.PositiveIntegerField(default = 0)
    purchased_quantity = models.PositiveIntegerField(default = 0)
    rating_average = models.FloatField(default=0)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.compress_image(self.image)
        super(Product, self).save(*args, **kwargs)

    def compress_image(self, uploaded_image):
        img = Image.open(uploaded_image)
        outputIoStream = BytesIO()
        img = img.resize((400, 400))
        img.save(outputIoStream , format='JPEG', quality=80)
        outputIoStream.seek(0)
        uploaded_image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % uploaded_image.name.split('.')[0], 'image/jpeg', None, None)
        return uploaded_image


class ProductRating(models.Model):
    rating = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_rating')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rating')

    class Meta():
        ordering=['id']
        unique_together = (("user", "product"),)

    def __str__(self):
        return '{}-{}'.format(str(self.product), str(self.rating))


@receiver(post_save, sender=ProductRating)
def update_average(sender, instance, **kwargs):
    product = instance.product
    product.rating_average = product.rating.all().aggregate(Avg('rating'))['rating__avg']
    product.save(update_fields=['rating_average'])

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(max_length=1000)
    date = models.DateTimeField(default=datetime.now, verbose_name='Date')

    class Meta():
        ordering=['id']

    def __str__(self):
        return '{} review .User {}'.format(str(self.product), str(self.user))
