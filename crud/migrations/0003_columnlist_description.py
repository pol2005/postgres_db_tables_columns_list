# Generated by Django 3.0.3 on 2020-03-01 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0002_auto_20200229_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='columnlist',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]