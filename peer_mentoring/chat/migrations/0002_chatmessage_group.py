# Generated by Django 4.1.6 on 2023-06-16 15:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("groups", "0014_alter_comment_options_alter_post_options_and_more"),
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatmessage",
            name="group",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="groups.group",
            ),
            preserve_default=False,
        ),
    ]
