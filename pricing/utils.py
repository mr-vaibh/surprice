from .models import DefaultPricing, PricingOverride

def calculate_price(sport, duration, booking_date, booking_time):
    default_price = DefaultPricing.objects.get(sport=sport, duration=duration).price
    
    # Apply overrides in order of priority
    overrides = PricingOverride.objects.filter(sport=sport)
    applicable_override = None

    # Date and Time
    applicable_override = overrides.filter(
        override_type='datetime',
        date=booking_date,
        start_time__lte=booking_time,
        end_time__gte=booking_time
    ).first()

    # Day and Time
    if not applicable_override:
        weekday = booking_date.weekday()  # 0=Monday, 6=Sunday
        applicable_override = overrides.filter(
            override_type='daytime',
            day_of_week=weekday,
            start_time__lte=booking_time,
            end_time__gte=booking_time
        ).first()

    # Time of Day
    if not applicable_override:
        applicable_override = overrides.filter(
            override_type='timeonly',
            start_time__lte=booking_time,
            end_time__gte=booking_time
        ).first()

    if applicable_override:
        return default_price + applicable_override.price_modifier
    
    return default_price
