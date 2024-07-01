# Generated by Django 5.0.6 on 2024-07-01 18:40

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_tasks', '0003_reviewstage_alter_task_review_stage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
