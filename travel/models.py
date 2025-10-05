from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class TravelOption(models.Model):
    TYPE_CHOICES = [
        ('FLIGHT', 'Flight'),
        ('TRAIN', 'Train'),
        ('BUS', 'Bus'),
    ]
    travel_id = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    source = models.CharField(max_length=120)
    destination = models.CharField(max_length=120)
    departure_datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.travel_id} • {self.type} • {self.source}->{self.destination}"

    def get_absolute_url(self):
        return reverse("travel:detail", args=[self.pk])


class Booking(models.Model):
    STATUS_CHOICES = [
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    ]
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE)
    number_of_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="CONFIRMED")
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True, default="")
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Booking {self.booking_id} by {self.user}"
    
    def can_cancel(self):
        """Check if booking can be cancelled (not already cancelled and departure is in future)"""
        from django.utils import timezone
        if self.status == 'CANCELLED':
            return False
        # Allow cancellation if departure is at least 2 hours away
        time_until_departure = self.travel_option.departure_datetime - timezone.now()
        return time_until_departure.total_seconds() > 7200  # 2 hours
    
    def calculate_refund(self):
        """Calculate refund amount based on cancellation policy"""
        from django.utils import timezone
        from decimal import Decimal, ROUND_HALF_UP
        
        time_until_departure = self.travel_option.departure_datetime - timezone.now()
        hours_until = time_until_departure.total_seconds() / 3600
        
        if hours_until >= 48:  # More than 48 hours
            refund = self.total_price * Decimal('0.9')  # 90% refund (10% cancellation fee)
        elif hours_until >= 24:  # 24-48 hours
            refund = self.total_price * Decimal('0.7')  # 70% refund
        elif hours_until >= 2:  # 2-24 hours
            refund = self.total_price * Decimal('0.5')  # 50% refund
        else:
            refund = Decimal('0')  # No refund
        
        # Round to 2 decimal places to match DecimalField constraints
        return refund.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def clean(self):
        """
        Ensure valid seat count. Only check availability if travel_option is attached.
        """
        if self.number_of_seats is None:
            return
        if self.number_of_seats < 1:
            raise ValidationError({"number_of_seats": "Number of seats must be at least 1."})
        if getattr(self, "travel_option_id", None):
            if self.number_of_seats > self.travel_option.available_seats:
                raise ValidationError({
                    "number_of_seats": f"Only {self.travel_option.available_seats} seats available."
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    """Extended user profile with additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Information
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say')
    ], blank=True)
    
    # Address Information
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True, default='USA')
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Travel Preferences
    preferred_travel_type = models.CharField(max_length=10, choices=[
        ('FLIGHT', 'Flight'),
        ('TRAIN', 'Train'),
        ('BUS', 'Bus'),
        ('ANY', 'No Preference')
    ], default='ANY', blank=True)
    
    # Profile Settings
    bio = models.TextField(max_length=500, blank=True)
    newsletter_subscription = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_full_address(self):
        """Return formatted full address"""
        parts = [
            self.address_line1,
            self.address_line2,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ]
        return ', '.join(filter(None, parts))
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


# Signal to automatically create/update user profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when user is created"""
    if created:
        UserProfile.objects.create(user=instance)
