# Generated by Django 4.2.2 on 2023-06-28 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_api', '0014_rename_new_price_product_saleprice_product_datefrom_and_more'),
        ('orders_api', '0004_alter_orderproduct_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='product_api.product'),
        ),
    ]
