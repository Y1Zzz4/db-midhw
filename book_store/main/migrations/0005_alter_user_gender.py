# Generated by Django 3.2.25 on 2025-05-05 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20250505_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', '男'), ('female', '女'), ('none', '无')], default='none', max_length=10),
        ),
    ]
