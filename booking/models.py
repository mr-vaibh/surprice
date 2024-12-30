from django.db import models
from django.db.models import Q
from pricing.models import Sport

# Create your models here.

class Booking(models.Model):
    customer_name = models.CharField(max_length=100)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    booking_datetime = models.DateTimeField()
    duration = models.IntegerField()  # Duration in minutes
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calculate_total_price(self):
        # Get the default pricing for the sport based on duration
        default_prices = self.sport.default_pricing.all()
        applicable_price = None

        # Find the first applicable price based on duration
        for pricing in default_prices:
            if pricing.duration >= int(self.duration):
                applicable_price = pricing.price
                break

        # If no price is found, take the highest price
        if not applicable_price:
            applicable_price = default_prices.last().price

        # Check for any applicable pricing overrides
        applicable_overrides = self.sport.pricing_overrides.filter(
            Q(date=self.booking_datetime.date()) |
            Q(day_of_week=self.booking_datetime.isoweekday()) |
            (Q(start_time__lte=self.booking_datetime.time()) & Q(end_time__gte=self.booking_datetime.time()))
        )

        price_modifier = 0
        applied_override = None  # To track which override was applied

        for override in applicable_overrides:
            # Apply the datetime-based override if it matches
            if override.override_type == 'datetime' and override.date == self.booking_datetime.date():
                price_modifier = override.price_modifier
                applied_override = 'datetime'
                break  # Exit as soon as a datetime override is applied

        if not applied_override:
            for override in applicable_overrides:
                # Apply the daytime-based override if it matches
                if override.override_type == 'daytime' and override.day_of_week == self.booking_datetime.isoweekday():
                    price_modifier = override.price_modifier
                    applied_override = 'daytime'
                    break  # Exit as soon as a daytime override is applied

        if not applied_override:
            for override in applicable_overrides:
                # Apply the timeonly-based override if it matches
                if override.override_type == 'timeonly' and override.start_time <= self.booking_datetime.time() <= override.end_time:
                    price_modifier = override.price_modifier
                    applied_override = 'timeonly'
                    break  # Exit as soon as a timeonly override is applied

        # If no override was applied, use the default applicable price
        if not applied_override:
            price_modifier = 0  # No price modification, use base price

        # Apply the price modifier to the base price
        total_price = applicable_price + price_modifier
        self.total_price = total_price
        self.save()

        # Print details for debugging
        print(f"Applicable Price: {applicable_price}")
        print(f"Price Modifier: {price_modifier}")
        print(f"Total Price: {total_price}")

        return total_price
