# Generated by Django 3.1.1 on 2020-09-17 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license', '0008_auto_20200916_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='is_send',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
