# Generated by Django 5.1.1 on 2024-09-05 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KenetAssets', '0005_dispatch_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consignment',
            name='slk_id',
            field=models.CharField(blank=True, editable=False, max_length=20, unique=True),
        ),
    ]
