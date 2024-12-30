from django.db import models

class Sport(models.Model):
    name = models.CharField(max_length=100)

class DefaultPricing(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='default_pricing')
    duration = models.IntegerField()  # Duration in minutes
    price = models.DecimalField(max_digits=10, decimal_places=2)

class PricingOverride(models.Model):
    OVERRIDE_TYPES = [
        ('datetime', 'Date and Time'),
        ('daytime', 'Day and Time'),
        ('timeonly', 'Time of Day'),
    ]
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='pricing_overrides')
    override_type = models.CharField(max_length=10, choices=OVERRIDE_TYPES)
    date = models.DateField(null=True, blank=True)  # For 'datetime'
    day_of_week = models.IntegerField(null=True, blank=True)  # For 'daytime'
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2)
