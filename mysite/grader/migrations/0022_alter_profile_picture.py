# Generated by Django 4.2.9 on 2024-03-16 12:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("grader", "0021_contact_info"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="picture",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]
