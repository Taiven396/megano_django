# Generated by Django 4.2.2 on 2023-06-19 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='paymentType',
            field=models.CharField(choices=[('online', 'Online'), ('cash', 'Cash')], max_length=50),
        ),
    ]