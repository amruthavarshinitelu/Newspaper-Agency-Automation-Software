# Generated by Django 3.2.18 on 2023-04-30 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_customer_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryagent',
            name='salary',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='customer',
            name='Amount',
            field=models.IntegerField(default=0),
        ),
    ]
