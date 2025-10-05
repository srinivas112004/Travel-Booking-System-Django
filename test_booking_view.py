import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_booking.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from travel.models import TravelOption

def test_booking_view():
    client = Client()
    
    # Get a user and travel option
    user = User.objects.get(username='testuser')
    travel = TravelOption.objects.first()
    
    print(f"Testing booking for travel: {travel}")
    print(f"User: {user.username}")
    
    # Login the user
    client.force_login(user)
    
    # Test GET request to booking form
    print("\n--- Testing GET request to booking form ---")
    response = client.get(f'/travel/{travel.pk}/book/')
    print(f"GET Status Code: {response.status_code}")
    if response.status_code != 200:
        print(f"GET Error: {response.content.decode()}")
    else:
        print("GET request successful")
    
    # Test POST request to create booking
    print("\n--- Testing POST request to create booking ---")
    response = client.post(f'/travel/{travel.pk}/book/', {
        'number_of_seats': 2,
        'csrfmiddlewaretoken': client.get(f'/travel/{travel.pk}/book/').context['csrf_token']
    })
    print(f"POST Status Code: {response.status_code}")
    
    if response.status_code == 302:
        print(f"POST successful - Redirected to: {response.url}")
    else:
        print(f"POST Error: {response.content.decode()}")
        
        # Check for form errors
        if hasattr(response, 'context') and response.context:
            form = response.context.get('form')
            if form and form.errors:
                print(f"Form errors: {form.errors}")

if __name__ == "__main__":
    test_booking_view()