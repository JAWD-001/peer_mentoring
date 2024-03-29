# Generated by Django 4.1.6 on 2023-05-22 03:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("groups", "0011_alter_groupjoinrequest_receiver_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="banned_users",
            field=models.ManyToManyField(
                related_name="banned_from_groups", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
