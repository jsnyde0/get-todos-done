from django.core.management.base import BaseCommand
from django.db import connection
import logging
import os

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Checks database connection and tables'

    def handle(self, *args, **options):
        from django.conf import settings
        db_path = settings.DATABASES['default']['NAME']
        self.stdout.write(f"Database path: {db_path}")
        logger.info(f"Database path: {db_path}")

        if os.path.exists(db_path):
            self.stdout.write(self.style.SUCCESS(f"Database file exists. Size: {os.path.getsize(db_path)} bytes"))
            logger.info(f"Database file exists. Size: {os.path.getsize(db_path)} bytes")
        else:
            self.stdout.write(self.style.ERROR(f"Database file does not exist at {db_path}"))
            logger.error(f"Database file does not exist at {db_path}")
            return

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
            self.stdout.write(self.style.SUCCESS(f'Found tables: {tables}'))
            logger.info(f'Found tables: {tables}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Database check failed: {str(e)}'))
            logger.error(f"Database check failed: {str(e)}")