# Generated by Django 2.2.3 on 2019-08-23 18:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('capchine', '0015_search_code_accessed_byy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='search_code',
            name='accessed_byy',
        ),
        migrations.RemoveField(
            model_name='search_code',
            name='accessed_by',
        ),
        migrations.AddField(
            model_name='search_code',
            name='accessed_by',
            field=models.ManyToManyField(blank=True, related_name='accessed_codes', to=settings.AUTH_USER_MODEL),
        ),
    ]