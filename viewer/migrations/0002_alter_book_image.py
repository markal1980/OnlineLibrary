# Generated by Django 4.2.2 on 2023-06-21 18:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("viewer", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="image",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
