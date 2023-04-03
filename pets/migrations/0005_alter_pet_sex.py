# Generated by Django 4.2 on 2023-04-03 17:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0004_alter_pet_sex"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pet",
            name="sex",
            field=models.CharField(
                choices=[
                    ("Male", "Male"),
                    ("Female", "Female"),
                    ("Not informed", "Default"),
                ],
                default="Not informed",
                max_length=20,
            ),
        ),
    ]
