from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from travel.models import TravelPackage
import os

class Command(BaseCommand):
    help = 'Set up production database with admin user and sample data'

    def handle(self, *args, **options):
        # Create superuser if it doesn't exist
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser: {admin_username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Superuser {admin_username} already exists')
            )

        # Create sample travel packages if none exist
        if not TravelPackage.objects.exists():
            packages = [
                {
                    'name': 'Paris Adventure',
                    'description': 'Explore the romantic city of lights with guided tours to the Eiffel Tower, Louvre Museum, and charming Montmartre district.',
                    'price': 1299.99,
                    'duration_days': 7,
                    'available_slots': 10
                },
                {
                    'name': 'Tokyo Experience',
                    'description': 'Discover modern Japan with visits to ancient temples, bustling markets, and the iconic Mount Fuji.',
                    'price': 1899.99,
                    'duration_days': 10,
                    'available_slots': 8
                },
                {
                    'name': 'Bali Tropical Escape',
                    'description': 'Relax on pristine beaches, explore ancient temples, and enjoy traditional Balinese culture.',
                    'price': 999.99,
                    'duration_days': 5,
                    'available_slots': 15
                },
                {
                    'name': 'New York City Lights',
                    'description': 'Experience the Big Apple with Broadway shows, Central Park, and iconic skyline views.',
                    'price': 1599.99,
                    'duration_days': 6,
                    'available_slots': 12
                }
            ]
            
            for package_data in packages:
                TravelPackage.objects.create(**package_data)
                self.stdout.write(
                    self.style.SUCCESS(f'Created travel package: {package_data["name"]}')
                )
        else:
            self.stdout.write(
                self.style.WARNING('Travel packages already exist')
            )

        self.stdout.write(
            self.style.SUCCESS('Production setup completed successfully!')
        )