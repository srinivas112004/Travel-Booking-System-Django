from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from travel.models import TravelOption
import random

class Command(BaseCommand):
    help = 'Add specific travel options to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['FLIGHT', 'TRAIN', 'BUS'],
            help='Type of travel option to add',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of travel options to add',
        )
        parser.add_argument(
            '--source',
            type=str,
            help='Source city',
        )
        parser.add_argument(
            '--destination',
            type=str,
            help='Destination city',
        )

    def handle(self, *args, **options):
        travel_type = options.get('type')
        count = options['count']
        source_filter = options.get('source')
        destination_filter = options.get('destination')
        
        # Sample cities
        cities = [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
            'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
            'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte',
            'San Francisco', 'Indianapolis', 'Seattle', 'Denver', 'Washington DC',
            'Boston', 'El Paso', 'Nashville', 'Detroit', 'Oklahoma City',
            'Portland', 'Las Vegas', 'Memphis', 'Louisville', 'Baltimore',
            'Miami', 'Atlanta', 'Tampa', 'Orlando', 'Minneapolis', 'Cleveland',
            'Pittsburgh', 'Cincinnati', 'Kansas City', 'Milwaukee', 'Buffalo'
        ]
        
        travel_options = []
        
        # Generate data based on type
        for i in range(count):
            if source_filter:
                source = source_filter
            else:
                source = random.choice(cities)
                
            if destination_filter:
                destination = destination_filter
            else:
                destination = random.choice([city for city in cities if city != source])
            
            # Generate departure time between now and 30 days from now
            departure = timezone.now() + timedelta(
                days=random.randint(1, 30),
                hours=random.randint(6, 23),
                minutes=random.choice([0, 15, 30, 45])
            )
            
            if not travel_type or travel_type == 'FLIGHT':
                airlines = ['American Airlines', 'Delta', 'United', 'Southwest', 'JetBlue', 'Alaska', 'Spirit', 'Frontier']
                airline = random.choice(airlines)
                travel_id = f"{airline[:2].upper()}{random.randint(100, 9999)}"
                
                travel_options.append(TravelOption(
                    travel_id=travel_id,
                    type='FLIGHT',
                    source=source,
                    destination=destination,
                    departure_datetime=departure,
                    price=random.randint(150, 800),
                    available_seats=random.randint(50, 200)
                ))
                
            if not travel_type or travel_type == 'TRAIN':
                train_companies = ['Amtrak', 'Metro-North', 'LIRR', 'Caltrain', 'NJ Transit', 'MBTA', 'VRE']
                company = random.choice(train_companies)
                travel_id = f"{company[:3].upper()}{random.randint(100, 999)}"
                
                travel_options.append(TravelOption(
                    travel_id=travel_id,
                    type='TRAIN',
                    source=source,
                    destination=destination,
                    departure_datetime=departure,
                    price=random.randint(50, 300),
                    available_seats=random.randint(100, 400)
                ))
                
            if not travel_type or travel_type == 'BUS':
                bus_companies = ['Greyhound', 'Megabus', 'FlixBus', 'Peter Pan', 'BoltBus', 'RedCoach', 'Concord Coach']
                company = random.choice(bus_companies)
                travel_id = f"{company[:3].upper()}{random.randint(100, 999)}"
                
                travel_options.append(TravelOption(
                    travel_id=travel_id,
                    type='BUS',
                    source=source,
                    destination=destination,
                    departure_datetime=departure,
                    price=random.randint(25, 150),
                    available_seats=random.randint(30, 60)
                ))
        
        # If specific type was requested, filter the list
        if travel_type:
            travel_options = [option for option in travel_options if option.type == travel_type]
        
        # Bulk create travel options
        TravelOption.objects.bulk_create(travel_options)
        
        # Print summary
        if travel_type:
            created_count = len(travel_options)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {created_count} {travel_type.lower()}s!')
            )
        else:
            flights_count = len([o for o in travel_options if o.type == 'FLIGHT'])
            trains_count = len([o for o in travel_options if o.type == 'TRAIN'])
            buses_count = len([o for o in travel_options if o.type == 'BUS'])
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {flights_count} flights, '
                    f'{trains_count} trains, and {buses_count} buses!'
                )
            )
        
        total_count = TravelOption.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'Total travel options in database: {total_count}')
        )