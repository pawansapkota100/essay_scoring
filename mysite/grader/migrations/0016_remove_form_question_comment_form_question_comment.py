# Generated by Django 4.2.9 on 2024-02-25 03:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("grader", "0015_remove_form_question_tags_form_question_tags"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="form_question",
            name="Comment",
        ),
        migrations.AddField(
            model_name="form_question",
            name="Comment",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="comments", to="grader.comment"
            ),
        ),
    ]