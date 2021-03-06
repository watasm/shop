# Generated by Django 2.2.3 on 2019-07-14 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20190714_0724'),
        ('coupons', '0005_auto_20190711_0839'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellercoupon',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coupons', to='orders.Order'),
        ),
        migrations.AlterField(
            model_name='sellercoupon',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
