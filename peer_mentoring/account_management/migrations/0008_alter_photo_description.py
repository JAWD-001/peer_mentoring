# Generated by Django 4.1.6 on 2023-07-21 07:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account_management", "0007_friendrequest_accepted"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="description",
            field=models.CharField(max_length=200, null=True),
        ),
    ]
