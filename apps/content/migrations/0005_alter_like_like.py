# Generated by Django 5.1.6 on 2025-02-19 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_alter_like_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='like',
            field=models.BooleanField(default=False),
        ),
    ]
