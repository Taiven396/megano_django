# Generated by Django 4.2.2 on 2023-06-16 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_api', '0004_product_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='free_delivery',
            new_name='freeDelivery',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='full_description',
            new_name='fullDescription',
        ),
    ]
