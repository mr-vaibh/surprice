from django.test import TestCase, Client
from pricing.models import Sport
from booking.models import Booking
from datetime import datetime

class BookingViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.sport = Sport.objects.create(name="Football")
        self.sport.default_pricing.create(duration=60, price=100)

    def test_create_booking(self):
        response = self.client.post(
            '/booking/create/',
            {
                'customer_name': 'Jane Doe',
                'sport_id': self.sport.id,
                'booking_datetime': '2024-12-31T15:00',
                'duration': 90
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_price', response.json())

    def test_invalid_sport_id(self):
        response = self.client.post(
            '/booking/create/',
            {
                'customer_name': 'Invalid Sport',
                'sport_id': 999,
                'booking_datetime': '2024-12-31T15:00',
                'duration': 90
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())