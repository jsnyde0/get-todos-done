# Generated by Django 5.0.6 on 2024-07-01 09:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_tasks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='category',
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(blank=True, choices=[(1, 'Low'), (2, 'Medium'), (3, 'High'), (4, 'Urgent')], default=2, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='review_stage',
            field=models.CharField(blank=True, choices=[('INBOX', 'Inbox'), ('DAILY', 'Review Daily'), ('WEEKLY', 'Review Weekly'), ('MONTHLY', 'Review Monthly'), ('QUARTERLY', 'Review Quarterly'), ('PLANNED', 'Subtask in Review/Planned'), ('SOMEDAY', 'Someday'), ('MAYBE', 'Maybe')], default='INBOX', max_length=10, null=True),
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Boards',
            },
        ),
        migrations.AddField(
            model_name='task',
            name='board',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='a_tasks.board'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]