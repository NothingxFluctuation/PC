# Generated by Django 2.2.3 on 2019-08-22 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capchine', '0010_auto_20190822_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='rated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
