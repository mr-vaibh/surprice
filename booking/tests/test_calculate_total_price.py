from django.test import TestCase
from pricing.models import Sport, PricingOverride, DefaultPricing
from booking.models import Booking
from datetime import datetime, time

class CalculateTotalPriceTestCase(TestCase):
    def setUp(self):
        # Create a Sport
        self.sport = Sport.objects.create(name="Tennis")

        # Create Default Pricing
        self.default_pricing_1 = DefaultPricing.objects.create(
            sport=self.sport,
            duration=60,
            price=100
        )
        self.default_pricing_2 = DefaultPricing.objects.create(
            sport=self.sport,
            duration=120,
            price=180
        )

        # Create Pricing Overrides
        self.override_datetime = PricingOverride.objects.create(
            sport=self.sport,
            override_type="datetime",
            date=datetime(2024, 12, 25).date(),
            price_modifier=50
        )
        self.override_daytime = PricingOverride.objects.create(
            sport=self.sport,
            override_type="daytime",
            day_of_week=3,  # Wednesday
            price_modifier=30
        )
        self.override_timeonly = PricingOverride.objects.create(
            sport=self.sport,
            override_type="timeonly",
            start_time=time(9, 0),
            end_time=time(12, 0),
            price_modifier=20
        )

    def test_default_pricing_only(self):
        booking = Booking.objects.create(
            customer_name="John Doe",
            sport=self.sport,
            booking_datetime=datetime(2024, 12, 26, 5, 0),  # No override applies
            duration=60
        )
        total_price = booking.calculate_total_price()
        self.assertEqual(total_price, 100)  # Default pricing for 60 mins

    def test_datetime_override(self):
        booking = Booking.objects.create(
            customer_name="Jane Doe",
            sport=self.sport,
            booking_datetime=datetime(2024, 12, 25, 10, 0),  # Matches datetime override
            duration=60
        )
        total_price = booking.calculate_total_price()
        self.assertEqual(total_price, 150)  # Default (100) + Datetime Modifier (50)

    def test_daytime_override(self):
        booking = Booking.objects.create(
            customer_name="Tom Smith",
            sport=self.sport,
            booking_datetime=datetime(2024, 12, 18, 10, 0),  # Wednesday, matches daytime override
            duration=60
        )
        total_price = booking.calculate_total_price()
        self.assertEqual(total_price, 130)  # Default (100) + Daytime Modifier (30)

    def test_timeonly_override(self):
        booking = Booking.objects.create(
            customer_name="Lucy Brown",
            sport=self.sport,
            booking_datetime=datetime(2024, 12, 19, 10, 30),  # Matches timeonly override
            duration=60
        )
        total_price = booking.calculate_total_price()
        self.assertEqual(total_price, 120)  # Default (100) + Timeonly Modifier (20)

    def test_multiple_overrides_priority(self):
        booking = Booking.objects.create(
            customer_name="Mark Green",
            sport=self.sport,
            booking_datetime=datetime(2024, 12, 25, 10, 30),  # Matches datetime, daytime, and timeonly
            duration=60
        )
        total_price = booking.calculate_total_price()
        self.assertEqual(total_price, 150)  # Datetime (highest priority): Default (100) + Datetime Modifier (50)

    def test_duration_based_pricing(self):
        booking = Booking.objects.create(
            customer_name="Duration Test",
            sport=self.sport,
            booking_datetime=datetime(2024, 12, 26, 5, 0),  # No overrides apply
            duration=120
        )
        total_price = booking.calculate_total_price()
        self.assertEqual(total_price, 180)  # Default pricing for 120 mins
