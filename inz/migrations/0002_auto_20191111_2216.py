# Generated by Django 2.2.5 on 2019-11-11 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='image',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='inz.Picture'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30, null=True, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=30, null=True, verbose_name='last name'),
        ),
    ]