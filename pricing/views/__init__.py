from django.shortcuts import render

from ..models import Sport
from ..utils import calculate_price

from datetime import datetime

def manage_pricing(request):
    return render(request, 'pricing/manage_pricing.html')