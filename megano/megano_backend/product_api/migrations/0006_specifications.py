# Generated by Django 4.2.2 on 2023-06-16 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_api', '0005_rename_free_delivery_product_freedelivery_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name': 'Спецификация',
                'verbose_name_plural': 'Спецификации',
            },
        ),
    ]