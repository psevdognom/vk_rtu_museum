# Generated by Django 2.2.3 on 2019-09-23 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('музей', '0002_auto_20190923_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='mark',
            field=models.CharField(db_index=True, max_length=150),
        ),
    ]
