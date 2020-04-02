# Generated by Django 2.2.3 on 2020-04-01 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystays', '0002_auto_20200401_2033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stay',
            name='address',
        ),
        migrations.RemoveField(
            model_name='stay',
            name='keyword1',
        ),
        migrations.RemoveField(
            model_name='stay',
            name='keyword2',
        ),
        migrations.AddField(
            model_name='stay',
            name='keyword',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='stay',
            name='latitude',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=15),
        ),
        migrations.AddField(
            model_name='stay',
            name='longitude',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=15),
        ),
    ]
