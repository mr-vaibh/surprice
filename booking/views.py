import json
from django.shortcuts import render
from django.http import JsonResponse
from pricing.models import Sport
from .models import Booking
from datetime import datetime

def booking(request):
    sports = Sport.objects.all()
    bookings = Booking.objects.all()
    return render(request, 'booking/create_booking.html', {'sports': sports, 'bookings': bookings})

def create_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            customer_name = data['customer_name']
            sport_id = data['sport_id']
            booking_datetime = data['booking_datetime']
            duration = data['duration']

            booking_datetime = datetime.strptime(booking_datetime, '%Y-%m-%dT%H:%M')

            sport = Sport.objects.get(id=sport_id)

            booking = Booking.objects.create(
                customer_name=customer_name,
                sport=sport,
                booking_datetime=booking_datetime,
                duration=duration
            )

            total_price = booking.calculate_total_price()

            return JsonResponse({
                'customer_name': booking.customer_name,
                'sport_name': booking.sport.name,
                'booking_datetime': booking.booking_datetime,
                'duration': booking.duration,
                'total_price': total_price,
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Sport.DoesNotExist:
            return JsonResponse({'error': 'Sport not found'}, status=404)