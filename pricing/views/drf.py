from rest_framework.viewsets import ModelViewSet
from ..models import Sport, DefaultPricing, PricingOverride
from ..serializers import SportSerializer, DefaultPricingSerializer, PricingOverrideSerializer


class SportViewSet(ModelViewSet):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer


class DefaultPricingViewSet(ModelViewSet):
    queryset = DefaultPricing.objects.select_related('sport').all()
    serializer_class = DefaultPricingSerializer


class PricingOverrideViewSet(ModelViewSet):
    queryset = PricingOverride.objects.select_related('sport').all()
    serializer_class = PricingOverrideSerializer
