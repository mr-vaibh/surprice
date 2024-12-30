from django.contrib import admin
from .models import Sport, DefaultPricing, PricingOverride

class PricingOverrideInline(admin.TabularInline):
    model = PricingOverride
    extra = 1  # Number of empty forms displayed in the admin by default
    fields = ['override_type', 'date', 'day_of_week', 'start_time', 'end_time', 'price_modifier']
    readonly_fields = ['override_type', 'date', 'day_of_week', 'start_time', 'end_time', 'price_modifier']

class DefaultPricingAdmin(admin.ModelAdmin):
    list_display = ['price', 'duration']
    search_fields = ['price']

class SportAdmin(admin.ModelAdmin):
    list_display = ['name', 'default_pricing_price', 'default_pricing_duration']
    inlines = [PricingOverrideInline]  # Display pricing overrides inline
    search_fields = ['name']  # Allow searching by name

    def default_pricing_price(self, obj):
        return obj.default_pricing.price  # Display the default price
    default_pricing_price.short_description = 'Default Price'  # Set custom column title

    def default_pricing_duration(self, obj):
        return obj.default_pricing.duration  # Display the default duration
    default_pricing_duration.short_description = 'Default Duration'  # Set custom column title

# Registering models and their custom admin views
admin.site.register(Sport, SportAdmin)
admin.site.register(DefaultPricing, DefaultPricingAdmin)
admin.site.register(PricingOverride)
