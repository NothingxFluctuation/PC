# Generated by Django 2.2.3 on 2019-08-22 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capchine', '0009_auto_20190822_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='attention',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rating',
            name='cooperation',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rating',
            name='performance',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rating',
            name='punctuality',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
