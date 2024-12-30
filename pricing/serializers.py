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
    
    def create(self, validated_data):
        # Handle creation of nested default_pricing
        default_pricing_data = validated_data.pop('default_pricing', None)
        pricing_overrides_data = validated_data.pop('pricing_overrides', [])

        # Create the Sport instance
        sport = Sport.objects.create(**validated_data)

        # Create the DefaultPricing instance if data is provided
        if default_pricing_data:
            default_pricing = DefaultPricing.objects.create(sport=sport, **default_pricing_data)
            sport.default_pricing = default_pricing

        # Create PricingOverride instances if any data is provided
        for override_data in pricing_overrides_data:
            PricingOverride.objects.create(sport=sport, **override_data)

        sport.save()  # Save the Sport instance after nested data is created
        return sport

    def update(self, instance, validated_data):
        # Update the simple fields
        instance.name = validated_data.get('name', instance.name)

        # Handle nested updates for default_pricing
        default_pricing_data = validated_data.get('default_pricing', None)

        if default_pricing_data:
            default_pricing_instance = instance.default_pricing
            DefaultPricingSerializer().update(default_pricing_instance, default_pricing_data)

        # Handle nested updates for pricing_overrides
        pricing_overrides_data = validated_data.get('pricing_overrides', [])
        for override_data in pricing_overrides_data:
            override_instance = PricingOverride.objects.get(id=override_data['id'])
            PricingOverrideSerializer().update(override_instance, override_data)

        instance.save()
        return instance
