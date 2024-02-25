# Generated by Django 4.2.9 on 2024-02-24 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("grader", "0011_alter_comment_question_alter_comment_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="form_question",
            name="tags",
            field=models.ManyToManyField(blank=True, null=True, to="grader.tag"),
        ),
        migrations.AlterField(
            model_name="form_question",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]