# Generated by Django 3.0.5 on 2023-02-07 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('couriermanage', '0017_auto_20230207_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courier',
            name='sent',
            field=models.BooleanField(default=False),
        ),
    ]
