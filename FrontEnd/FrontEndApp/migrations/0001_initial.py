# Generated by Django 5.0.2 on 2024-05-07 03:01

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="sesion",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("token", models.CharField(default="", max_length=200)),
                ("rol", models.CharField(default="", max_length=200)),
            ],
        ),
    ]
