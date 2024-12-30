from django.contrib import admin
from .models import Sport, DefaultPricing, PricingOverride

class PricingOverrideInline(admin.TabularInline):
    model = PricingOverride
    extra = 1
    fields = ['override_type', 'date', 'day_of_week', 'start_time', 'end_time', 'price_modifier']

class DefaultPricingInline(admin.TabularInline):
    model = DefaultPricing
    extra = 1
    list_display = ['price', 'duration']
    fields = ['price', 'duration']

class SportAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [DefaultPricingInline, PricingOverrideInline]
    search_fields = ['name']

# Registering models and their custom admin views
admin.site.register(Sport, SportAdmin)
admin.site.register(DefaultPricing)
admin.site.register(PricingOverride)
