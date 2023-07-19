# Generated by Django 4.2.2 on 2023-07-06 21:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product_api", "0002_specifications_product"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="specifications",
        ),
        migrations.AddField(
            model_name="product",
            name="specifications",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="specifications",
                to="product_api.specifications",
            ),
        ),
    ]
