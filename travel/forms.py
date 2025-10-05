from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Booking, TravelOption
from django.core.exceptions import ValidationError

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["number_of_seats"]
        widgets = {"number_of_seats": forms.NumberInput(attrs={"min": 1})}

    def __init__(self, *args, travel_option: TravelOption = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.travel_option = travel_option

    def clean_number_of_seats(self):
        seats = self.cleaned_data.get("number_of_seats")
        if seats is None or seats < 1:
            raise ValidationError("Number of seats must be at least 1.")
        if self.travel_option and seats > self.travel_option.available_seats:
            raise ValidationError(f"Only {self.travel_option.available_seats} seats available.")
        return seats
