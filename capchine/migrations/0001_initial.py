# Generated by Django 2.2.3 on 2019-08-09 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_count', models.IntegerField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('u', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tchr_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_count', models.IntegerField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('u', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stdnt_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Search_Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200)),
                ('rating', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('accessed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accessed_codes', to=settings.AUTH_USER_MODEL)),
                ('u', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_srch_code', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='given_rating', to=settings.AUTH_USER_MODEL)),
                ('u', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_rating', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]