# Generated by Django 4.2.2 on 2023-06-16 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_api', '0008_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='reviews',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product_api.review'),
        ),
    ]