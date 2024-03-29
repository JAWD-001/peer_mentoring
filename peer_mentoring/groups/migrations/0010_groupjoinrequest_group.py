# Generated by Django 4.1.6 on 2023-05-19 14:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("groups", "0009_groupjoinrequest_created_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="groupjoinrequest",
            name="group",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="groups.group",
            ),
            preserve_default=False,
        ),
    ]
