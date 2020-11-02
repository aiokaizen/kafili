# Generated by Django 2.2 on 2020-10-31 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orphanage', '0009_auto_20201031_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='guardian',
            name='first_name_ar',
            field=models.CharField(blank=True, default='', max_length=57, verbose_name='الإسم الشخصي بالعربية'),
        ),
        migrations.AddField(
            model_name='guardian',
            name='last_name_ar',
            field=models.CharField(blank=True, default='', max_length=57, verbose_name='الإسم العائلي بالعربية'),
        ),
    ]