# Generated by Django 3.2.5 on 2022-06-19 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_alter_order_ordered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]