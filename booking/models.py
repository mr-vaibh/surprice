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
        '''Calculate the total price of the booking based on the sport's pricing rules'''

        default_prices = self.sport.default_pricing.all()
        applicable_price = None

        # Find the applicable price based on duration
        for pricing in default_prices:
            if pricing.duration >= int(self.duration):
                applicable_price = pricing.price
                break

        # If no price is found, take the highest price
        if not applicable_price:
            applicable_price = default_prices.last().price

        # Separate the pricing overrides by type
        applicable_overrides_datetime = self.sport.pricing_overrides.filter(
            Q(override_type='datetime') & Q(date=self.booking_datetime.date())
        )
        applicable_overrides_daytime = self.sport.pricing_overrides.filter(
            Q(override_type='daytime') & Q(day_of_week=self.booking_datetime.isoweekday())
        )
        applicable_overrides_timeonly = self.sport.pricing_overrides.filter(
            Q(override_type='timeonly') & 
            Q(start_time__lte=self.booking_datetime.time()) & 
            Q(end_time__gte=self.booking_datetime.time())
        )

        price_modifier = 0
        applied_override = None

        # Process overrides in hierarchical order
        if applicable_overrides_datetime.exists():
            override = applicable_overrides_datetime.first()
            price_modifier = override.price_modifier
            applied_override = 'datetime'
        elif applicable_overrides_daytime.exists():
            override = applicable_overrides_daytime.first()
            price_modifier = override.price_modifier
            applied_override = 'daytime'
        elif applicable_overrides_timeonly.exists():
            override = applicable_overrides_timeonly.first()
            price_modifier = override.price_modifier
            applied_override = 'timeonly'

        # Apply the price modifier to the base price
        total_price = applicable_price + price_modifier
        self.total_price = total_price
        self.save()

        print(f"Applicable Price: {applicable_price}")
        print(f"Price Modifier: {price_modifier}")
        print(f"Applied Override: {applied_override}")
        print(f"Total Price: {total_price}")

        return total_price
