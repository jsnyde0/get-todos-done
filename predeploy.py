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

from django.db import connection
import logging
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_database():
    db_path = settings.DATABASES['default']['NAME']
    logger.info(f"Checking database at: {db_path}")
    
    if os.path.exists(db_path):
        logger.info(f"Database file exists. Size: {os.path.getsize(db_path)} bytes")
        # Check if it's readable and writable
        if os.access(db_path, os.R_OK | os.W_OK):
            logger.info("Database file is readable and writable")
        else:
            logger.warning("Database file permissions issue")
    else:
        logger.warning(f"Database file does not exist at {db_path}")
        # Try to create an empty file
        try:
            open(db_path, 'a').close()
            logger.info("Created an empty database file")
        except Exception as e:
            logger.error(f"Failed to create database file: {str(e)}")

def main():
    logger.info("Waiting for 5 seconds before running migrations...")
    time.sleep(5)

    try:
        logger.info("Starting migrations...")
        call_command('makemigrations')
        call_command('migrate')
        logger.info("Migrations completed successfully.")

        # ... (rest of the function)

        logger.info("All predeploy tasks completed successfully!")
    except Exception as e:
        logger.error(f"An error occurred during predeploy: {str(e)}")
        raise  # Re-raise the exception to ensure the deploy fails if there's an error
    
    # Perform a simple database query to ensure it's accessible
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        logger.info(f"Database check result: {result}")

    check_database()

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
    Site.objects.get_or_create(
        id=1,
        defaults={'domain': 'gettingtasksdone.com', 'name': 'Getting Tasks Done'}
    )
    

    # Create default boards and review stages
    create_default_boards(user=first_user)
    create_default_review_stages()

    print("Predeploy tasks completed successfully!")

if __name__ == "__main__":
    main()