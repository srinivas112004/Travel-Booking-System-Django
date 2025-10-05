"""
Diagnostic script to identify the booking error
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_booking.settings')
django.setup()

from django.contrib.auth.models import User
from travel.models import TravelOption

def diagnose_booking_issue():
    print("=== TRAVEL BOOKING DIAGNOSTIC ===\n")
    
    # Check if there are travel options
    travel_count = TravelOption.objects.count()
    print(f"✓ Travel options in database: {travel_count}")
    
    if travel_count == 0:
        print("❌ ERROR: No travel options found! Run 'python manage.py populate_travel_data' first.")
        return
    
    # Check if there are users
    user_count = User.objects.count()
    print(f"✓ Users in database: {user_count}")
    
    if user_count == 0:
        print("❌ ERROR: No users found! Users need to register first.")
        return
    
    # Get sample data
    sample_travel = TravelOption.objects.first()
    sample_user = User.objects.first()
    
    print(f"✓ Sample travel option: {sample_travel}")
    print(f"✓ Sample user: {sample_user.username}")
    print(f"✓ Available seats: {sample_travel.available_seats}")
    
    # Check URL patterns
    print(f"\n📍 URL to test booking: http://127.0.0.1:8000/travel/{sample_travel.pk}/book/")
    print(f"📍 Direct travel detail URL: http://127.0.0.1:8000/travel/{sample_travel.pk}/")
    
    print("\n=== COMMON BOOKING ISSUES ===")
    print("1. ❗ User not logged in - The booking view requires authentication")
    print("   Solution: Go to http://127.0.0.1:8000/login/ to log in first")
    print("   Or register at: http://127.0.0.1:8000/register/")
    
    print("\n2. ❗ No available seats")
    print("   Solution: Check that available_seats > 0")
    
    print("\n3. ❗ Form validation errors")
    print("   Solution: Ensure you're entering valid number of seats")
    
    print("\n=== TESTING STEPS ===")
    print("1. Go to: http://127.0.0.1:8000/")
    print("2. Click 'Register' or 'Login'")
    print("3. Browse travel options")
    print("4. Click on a travel option")
    print("5. Click 'Book Now'")
    print("6. Enter number of seats and submit")
    
    print(f"\n=== QUICK TEST CREDENTIALS ===")
    print("Username: testuser")
    print("Password: testpass123")

if __name__ == "__main__":
    diagnose_booking_issue()