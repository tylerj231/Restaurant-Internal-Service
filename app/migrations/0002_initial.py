# Generated by Django 5.1.6 on 2025-02-10 15:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("app", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="vote",
            name="employee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="votes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="vote",
            name="menu",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="votes",
                to="app.dailymenu",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="dailymenu",
            unique_together={("restaurant", "date")},
        ),
        migrations.AlterUniqueTogether(
            name="vote",
            unique_together={("menu", "employee")},
        ),
    ]
