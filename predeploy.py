import os
import django
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a_core.settings")
django.setup()

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
    defaults={'domain': 'gettasksdone.com', 'name': 'Get Tasks Done'}
)

print("Predeploy tasks completed successfully!")