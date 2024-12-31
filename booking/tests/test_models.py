from django.test import TestCase
from pricing.models import Sport, PricingOverride, DefaultPricing
from booking.models import Booking
from datetime import datetime, time

class BookingModelTestCase(TestCase):
    def setUp(self):
        self.sport = Sport.objects.create(name="Tennis")
        self.default_pricing_1 = DefaultPricing.objects.create(
            sport=self.sport,
            duration=60,
            price=100
        )
        self.override_daytime = PricingOverride.objects.create(
            sport=self.sport,
            override_type="daytime",
            day_of_week=3,  # Wednesday
            price_modifier=50
        )
        self.booking = Booking.objects.create(
            customer_name="John Doe",
            sport=self.sport,
            booking_datetime=datetime(2024, 12, 31, 10, 0), # Not a Wednesday
            duration=60
        )

    # Not a Wednesday, no override applies
    def test_calculate_total_price_with_default_pricing(self):
        total_price = self.booking.calculate_total_price()
        self.assertEqual(total_price, 100)

    # Wednesday, override applies
    def test_calculate_total_price_with_override(self):
        self.booking.booking_datetime = datetime(2024, 12, 25, 10, 0)
        self.booking.save()
        total_price = self.booking.calculate_total_price()
        self.assertEqual(total_price, 150)