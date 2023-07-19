# Generated by Django 4.2.2 on 2023-07-07 19:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product_api", "0003_remove_product_specifications_product_specifications"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="specifications",
            field=models.ManyToManyField(
                blank=True,
                related_name="specifications",
                to="product_api.specifications",
            ),
        ),
    ]
