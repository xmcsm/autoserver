# Generated by Django 2.2.12 on 2020-06-03 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('respository', '0005_auto_20200602_0844'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='changelog',
            options={'verbose_name_plural': '资产变更表'},
        ),
        migrations.AlterField(
            model_name='cpu',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpu', to='respository.Server'),
        ),
        migrations.AlterField(
            model_name='errorlog',
            name='server',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='el', to='respository.Server'),
        ),
        migrations.AlterField(
            model_name='mem',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mem', to='respository.Server'),
        ),
        migrations.AlterField(
            model_name='server',
            name='hostname',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='主机名'),
        ),
        migrations.AlterField(
            model_name='server',
            name='is_sync',
            field=models.IntegerField(choices=[(0, '未同步'), (1, '已同步')], default=0, verbose_name='同步状态'),
        ),
        migrations.AlterField(
            model_name='server',
            name='os_version',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='操作系统版本'),
        ),
    ]
