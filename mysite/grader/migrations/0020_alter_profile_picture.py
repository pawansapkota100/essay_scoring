# Generated by Django 4.2.9 on 2024-03-02 07:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("grader", "0019_alter_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="picture",
            field=models.ImageField(default="images/default.png", upload_to=""),
        ),
    ]