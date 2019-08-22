# Generated by Django 2.2.3 on 2019-08-22 09:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('capchine', '0008_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='search_code',
            name='accessed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='search_code',
            name='accessed_by',
        ),
        migrations.AddField(
            model_name='search_code',
            name='accessed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accessed_code', to=settings.AUTH_USER_MODEL),
        ),
    ]
