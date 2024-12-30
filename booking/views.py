import json
from django.shortcuts import render
from django.http import JsonResponse
from pricing.models import Sport
from .models import Booking
from datetime import datetime

def create_booking(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))
            
            customer_name = data.get('customer_name', 'Anonymous')
            sport_id = int(data.get('sport_id', None))
            booking_datetime = data.get('booking_datetime', None)
            duration = data.get('duration', None)
            
            # Convert the booking_datetime string to a datetime object
            booking_datetime = datetime.strptime(booking_datetime, '%Y-%m-%dT%H:%M')

            sport = Sport.objects.get(id=sport_id)

            # Create the booking object
            booking = Booking.objects.create(
                customer_name=customer_name,
                sport=sport,
                booking_datetime=booking_datetime,
                duration=duration
            )

            # Calculate the total price
            total_price = booking.calculate_total_price()

            return JsonResponse({'total_price': total_price})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Sport.DoesNotExist:
            return JsonResponse({'error': 'Sport not found'}, status=404)
    
    sports = Sport.objects.all()
    bookings = Booking.objects.all()
    return render(request, 'booking/create_booking.html', {'sports': sports, 'bookings': bookings})

