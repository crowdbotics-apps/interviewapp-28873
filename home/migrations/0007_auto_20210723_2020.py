# Generated by Django 2.2.24 on 2021-07-23 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20210723_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='user',
            field=models.IntegerField(editable=False, null=True),
        ),
    ]
