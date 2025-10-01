from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Load initial users data if database is empty'

    def handle(self, *args, **options):
        from django.contrib.auth.models import User
        
        # Check if database is empty (no users exist)
        if not User.objects.exists():
            self.stdout.write('Loading initial users data...')
            try:
                call_command('loaddata', 'users_data.json')
                self.stdout.write(
                    self.style.SUCCESS('Initial users data loaded successfully!')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error loading users data: {e}')
                )
        else:
            self.stdout.write(
                self.style.WARNING('Database already has users. Skipping initial data load.')
            )