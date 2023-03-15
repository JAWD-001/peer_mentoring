# Generated by Django 4.1.6 on 2023-03-15 05:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("groups", "0002_remove_group_members"),
        ("account_management", "0003_alter_userprofile_avatar"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="groups_joined",
            field=models.ManyToManyField(to="groups.group"),
        ),
    ]
