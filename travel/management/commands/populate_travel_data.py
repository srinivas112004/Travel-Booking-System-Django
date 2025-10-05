from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from travel.models import TravelOption
import random

class Command(BaseCommand):
    help = 'Populate the database with sample travel data for flights, buses, and trains'

    def handle(self, *args, **options):
        # Clear existing data
        TravelOption.objects.all().delete()
        
        # Sample cities
        cities = [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
            'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
            'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte',
            'San Francisco', 'Indianapolis', 'Seattle', 'Denver', 'Washington DC',
            'Boston', 'El Paso', 'Nashville', 'Detroit', 'Oklahoma City',
            'Portland', 'Las Vegas', 'Memphis', 'Louisville', 'Baltimore'
        ]
        
        # Generate sample data
        travel_options = []
        
        # Flight data
        flight_airlines = ['American Airlines', 'Delta', 'United', 'Southwest', 'JetBlue', 'Alaska']
        for i in range(50):
            source = random.choice(cities)
            destination = random.choice([city for city in cities if city != source])
            airline = random.choice(flight_airlines)
            flight_number = f"{airline[:2].upper()}{random.randint(100, 9999)}"
            
            # Generate departure time between now and 30 days from now
            departure = timezone.now() + timedelta(
                days=random.randint(1, 30),
                hours=random.randint(6, 22),
                minutes=random.choice([0, 15, 30, 45])
            )
            
            travel_options.append(TravelOption(
                travel_id=flight_number,
                type='FLIGHT',
                source=source,
                destination=destination,
                departure_datetime=departure,
                price=random.randint(150, 800),
                available_seats=random.randint(50, 200)
            ))
        
        # Train data
        train_companies = ['Amtrak', 'Metro-North', 'LIRR', 'Caltrain', 'NJ Transit']
        for i in range(30):
            source = random.choice(cities)
            destination = random.choice([city for city in cities if city != source])
            company = random.choice(train_companies)
            train_number = f"{company[:3].upper()}{random.randint(100, 999)}"
            
            departure = timezone.now() + timedelta(
                days=random.randint(1, 15),
                hours=random.randint(6, 23),
                minutes=random.choice([0, 15, 30, 45])
            )
            
            travel_options.append(TravelOption(
                travel_id=train_number,
                type='TRAIN',
                source=source,
                destination=destination,
                departure_datetime=departure,
                price=random.randint(50, 300),
                available_seats=random.randint(100, 400)
            ))
        
        # Bus data
        bus_companies = ['Greyhound', 'Megabus', 'FlixBus', 'Peter Pan', 'BoltBus']
        for i in range(40):
            source = random.choice(cities)
            destination = random.choice([city for city in cities if city != source])
            company = random.choice(bus_companies)
            bus_number = f"{company[:3].upper()}{random.randint(100, 999)}"
            
            departure = timezone.now() + timedelta(
                days=random.randint(1, 10),
                hours=random.randint(6, 23),
                minutes=random.choice([0, 15, 30, 45])
            )
            
            travel_options.append(TravelOption(
                travel_id=bus_number,
                type='BUS',
                source=source,
                destination=destination,
                departure_datetime=departure,
                price=random.randint(25, 150),
                available_seats=random.randint(30, 60)
            ))
        
        # Bulk create all travel options
        TravelOption.objects.bulk_create(travel_options)
        
        # Print summary
        flights_count = TravelOption.objects.filter(type='FLIGHT').count()
        trains_count = TravelOption.objects.filter(type='TRAIN').count()
        buses_count = TravelOption.objects.filter(type='BUS').count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {flights_count} flights, '
                f'{trains_count} trains, and {buses_count} buses!'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Total travel options: {flights_count + trains_count + buses_count}'
            )
        )