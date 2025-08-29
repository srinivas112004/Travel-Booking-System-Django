from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import TravelOption, Booking
from django.utils import timezone
from django.urls import reverse

User = get_user_model()

class BookingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.travel = TravelOption.objects.create(
            travel_id='T1',
            type='BUS',
            source='A',
            destination='B',
            departure_datetime=timezone.now() + timezone.timedelta(days=1),
            price=100.00,
            available_seats=5
        )

    def test_booking_reduces_available_seats(self):
        self.client.login(username='testuser', password='pass')
        resp = self.client.post(reverse('travel:book', args=[self.travel.pk]), {'number_of_seats': 2})
        self.assertRedirects(resp, reverse('travel:my_bookings'))
        self.travel.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 3)
        self.assertEqual(Booking.objects.count(), 1)

    def test_cannot_overbook(self):
        self.client.login(username='testuser', password='pass')
        resp = self.client.post(reverse('travel:book', args=[self.travel.pk]), {'number_of_seats': 10})
        self.assertEqual(Booking.objects.count(), 0)
        self.travel.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 5)
        self.assertContains(resp, 'Only 5 seats', status_code=200)

    def test_cancel_restores_seats(self):
        b = Booking.objects.create(user=self.user, travel_option=self.travel, number_of_seats=2, total_price=200)
        self.travel.available_seats -= 2
        self.travel.save()
        self.client.login(username='testuser', password='pass')
        resp = self.client.get(reverse('travel:cancel_booking', args=[b.pk]))
        self.assertRedirects(resp, reverse('travel:my_bookings'))
        self.travel.refresh_from_db()
        b.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 5)
        self.assertEqual(b.status, 'CANCELLED')

class SearchFilterTests(TestCase):
    def setUp(self):
        TravelOption.objects.create(
            travel_id='F1', type='FLIGHT', source='Mumbai', destination='Delhi',
            departure_datetime=timezone.now() + timezone.timedelta(days=3), price=100, available_seats=10
        )
        TravelOption.objects.create(
            travel_id='T1', type='TRAIN', source='Chennai', destination='Bangalore',
            departure_datetime=timezone.now() + timezone.timedelta(days=4), price=50, available_seats=50
        )

    def test_search_by_destination(self):
        resp = self.client.get(reverse('travel:list') + '?destination=Delhi')
        self.assertContains(resp, 'Mumbai')
        self.assertNotContains(resp, 'Chennai')

    def test_filter_by_type(self):
        resp = self.client.get(reverse('travel:list') + '?type=TRAIN')
        self.assertContains(resp, 'Bangalore')
        self.assertNotContains(resp, 'Delhi')
