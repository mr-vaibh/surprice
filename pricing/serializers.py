from rest_framework import serializers
from .models import Sport, DefaultPricing, PricingOverride

class DefaultPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultPricing
        fields = ['id', 'sport', 'duration', 'price']

class PricingOverrideSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingOverride
        fields = [
            'id', 'sport', 'override_type', 'date', 'day_of_week',
            'start_time', 'end_time', 'price_modifier'
        ]

class SportSerializer(serializers.ModelSerializer):
    default_pricing = DefaultPricingSerializer(required=False, many=True)
    pricing_overrides = PricingOverrideSerializer(required=False, many=True)

    class Meta:
        model = Sport
        fields = ['id', 'name', 'default_pricing', 'pricing_overrides']