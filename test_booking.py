import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_booking.settings')
django.setup()

from travel.models import TravelOption, Booking
from django.contrib.auth.models import User

def test_booking():
    try:
        # Get a travel option
        travel = TravelOption.objects.first()
        if not travel:
            print("No travel options found!")
            return
            
        print(f"Testing booking for: {travel}")
        print(f"Available seats: {travel.available_seats}")
        print(f"Price: {travel.price}")
        
        # Get a user
        user = User.objects.first()
        if not user:
            print("No users found!")
            return
            
        print(f"User: {user.username}")
        
        # Try to create a booking
        seats = 2
        total_price = seats * travel.price
        
        print(f"Attempting to book {seats} seats for total ${total_price}")
        
        booking = Booking.objects.create(
            user=user,
            travel_option=travel,
            number_of_seats=seats,
            total_price=total_price,
        )
        
        print(f"Booking successful! ID: {booking.booking_id}")
        
        # Update available seats
        travel.available_seats -= seats
        travel.save()
        
        print(f"Updated available seats: {travel.available_seats}")
        
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_booking()