# Generated by Django 2.2.5 on 2019-10-18 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inz', '0002_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
