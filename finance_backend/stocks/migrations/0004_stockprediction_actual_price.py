# Generated by Django 5.1.2 on 2024-10-22 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0003_stockprediction'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockprediction',
            name='actual_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
