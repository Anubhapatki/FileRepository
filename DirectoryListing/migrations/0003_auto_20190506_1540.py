# Generated by Django 2.2.1 on 2019-05-06 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DirectoryListing', '0002_auto_20190506_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filerepository',
            name='archived_date',
            field=models.DateTimeField(),
        ),
    ]
