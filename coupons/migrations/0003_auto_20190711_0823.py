# Generated by Django 2.2.3 on 2019-07-11 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0002_sellercoupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellercoupon',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coupons', to='cart.Cart'),
        ),
    ]
