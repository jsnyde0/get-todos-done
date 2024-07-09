import os
import django
from django.core.management import call_command

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a_core.settings")

# Configure Django
django.setup()

# Now we can safely import Django models
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.conf import settings
from a_tasks.models import Board, ReviewStage

def create_default_boards(user):
    default_boards = ['Personal', 'Learning', 'Default']
    for board_name in default_boards:
        Board.objects.get_or_create(name=board_name, defaults={'user': user})

def create_default_review_stages(user):
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
        ReviewStage.objects.get_or_create(name=stage_name, defaults={'order': order, 'user': user})

def main():
    # Run migrations
    call_command('makemigrations')
    call_command('migrate')

    # Create superuser if it doesn't exist
    User = get_user_model()
    try:
        if not User.objects.filter(username=settings.SUPERUSER_USERNAME).exists():
            User.objects.create_superuser(
                settings.SUPERUSER_USERNAME,
                settings.SUPERUSER_EMAIL,
                settings.SUPERUSER_PASSWORD
            )
        first_user = User.objects.first()
        if not first_user:
            raise Exception("No users found in the database")
    except Exception as e:
        print(f"Error setting up user: {e}")
        return

    # Create or update Site object
    Site.objects.update_or_create(
        id=1,
        defaults={'domain': 'get-tasks-done.onrender.com', 'name': 'Get Tasks Done'}
    )

    # Create default boards and review stages
    create_default_boards(user=first_user)
    create_default_review_stages(user=first_user)

    print("Predeploy tasks completed successfully!")

if __name__ == "__main__":
    main()