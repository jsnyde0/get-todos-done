# Generated by Django 5.0.6 on 2024-07-05 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_tasks', '0004_alter_board_id_alter_tag_id_alter_task_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
