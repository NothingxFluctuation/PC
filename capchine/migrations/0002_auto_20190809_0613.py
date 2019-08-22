# Generated by Django 2.2.3 on 2019-08-09 01:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capchine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search_code',
            name='accessed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accessed_codes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='student',
            name='code_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='search_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
