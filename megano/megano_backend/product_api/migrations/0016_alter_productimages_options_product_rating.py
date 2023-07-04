# Generated by Django 4.2.2 on 2023-07-02 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_api', '0015_review_checked'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimages',
            options={'verbose_name': 'Изображение продукта', 'verbose_name_plural': 'Изображения продуктов'},
        ),
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
