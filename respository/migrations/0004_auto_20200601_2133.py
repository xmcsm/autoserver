# Generated by Django 2.2.12 on 2020-06-01 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('respository', '0003_auto_20200601_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='net',
            name='broadcast',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='广播地址'),
        ),
    ]
