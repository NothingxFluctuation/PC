# Generated by Django 2.2.3 on 2019-08-23 18:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capchine', '0016_auto_20190823_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search_code',
            name='accessed_by',
            field=models.ManyToManyField(blank=True, related_name='accessed_code', to=settings.AUTH_USER_MODEL),
        ),
    ]