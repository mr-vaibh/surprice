from django.shortcuts import render

def manage_pricing(request):
    return render(request, 'pricing/manage_pricing.html')