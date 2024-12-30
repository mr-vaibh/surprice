from django.urls import path
from .views import manage_pricing

from rest_framework.routers import DefaultRouter
from .views.drf import SportViewSet, DefaultPricingViewSet, PricingOverrideViewSet

router = DefaultRouter()
router.register(r'sports', SportViewSet, basename='sports')
router.register(r'default-pricing', DefaultPricingViewSet, basename='default-pricing')
router.register(r'pricing-overrides', PricingOverrideViewSet, basename='pricing-overrides')


urlpatterns = [
    path('manage-pricing/', manage_pricing, name='manage_pricing'),
]

urlpatterns += router.urls