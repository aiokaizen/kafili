# Generated by Django 2.2 on 2021-01-25 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orphanage', '0020_auto_20210124_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='mark_ceiling',
            field=models.PositiveSmallIntegerField(default=10, verbose_name='أعلى نقطة ممكنة'),
        ),
        migrations.AlterField(
            model_name='student',
            name='s1_decision',
            field=models.CharField(blank=True, choices=[('', 'إختر من القائمة'), ('F', 'راسب'), ('C', 'مقبول'), ('B', 'مستحسن'), ('A', 'حسن'), ('A+', 'حسن جدا')], default='', max_length=2, verbose_name='ميزة الدورة الأولى'),
        ),
        migrations.AlterField(
            model_name='student',
            name='s2_decision',
            field=models.CharField(blank=True, choices=[('', 'إختر من القائمة'), ('F', 'راسب'), ('C', 'مقبول'), ('B', 'مستحسن'), ('A', 'حسن'), ('A+', 'حسن جدا')], default='', max_length=2, verbose_name='ميزة الدورة الثانية'),
        ),
        migrations.AlterField(
            model_name='student',
            name='year_decision',
            field=models.CharField(blank=True, choices=[('', 'إختر من القائمة'), ('F', 'راسب'), ('C', 'مقبول'), ('B', 'مستحسن'), ('A', 'حسن'), ('A+', 'حسن جدا')], default='', max_length=2, verbose_name='ميزة السنة'),
        ),
    ]
