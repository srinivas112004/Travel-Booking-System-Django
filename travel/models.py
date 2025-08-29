from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid
from django.core.exceptions import ValidationError

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

    def __str__(self):
        return f"Booking {self.booking_id} by {self.user}"

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
