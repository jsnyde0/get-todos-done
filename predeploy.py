import os
import django
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a_core.settings")
django.setup()

from a_tasks.models import Board, ReviewStage  # Import your models

def create_default_boards():
    default_boards = ['Personal', 'Learning', 'Default']
    for board_name in default_boards:
        Board.objects.get_or_create(name=board_name, defaults={'user': None})

def create_default_review_stages():
    default_stages = [
        ('Inbox', 1),
        ('Review Daily', 2),
        ('Review Weekly', 3),
        ('Review Monthly', 4),
        ('Review Quarterly', 5),
        ('Subtask in Review / Planned', 6),
        ('Someday', 7),
        ('Maybe', 8)
    ]
    for stage_name, order in default_stages:
        ReviewStage.objects.get_or_create(name=stage_name, defaults={'order': order})

# Run migrations
call_command('makemigrations')
call_command('migrate')

# Create superuser if it doesn't exist
User = get_user_model()
if not User.objects.filter(username=settings.SUPERUSER_USERNAME).exists():
    User.objects.create_superuser(
        settings.SUPERUSER_USERNAME,
        settings.SUPERUSER_EMAIL,
        settings.SUPERUSER_PASSWORD
    )

# Create or update Site object
Site.objects.update_or_create(
    id=1,
    defaults={'domain': 'get-tasks-done.onrender.com', 'name': 'Get Tasks Done'}
)

# Create default boards and review stages
create_default_boards()
create_default_review_stages()

print("Predeploy tasks completed successfully!")