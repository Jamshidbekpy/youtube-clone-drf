# Generated by Django 5.1.6 on 2025-02-20 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_channel_owner'),
        ('content', '0006_comment_parent_delete_commentcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='accounts.channel'),
        ),
    ]
