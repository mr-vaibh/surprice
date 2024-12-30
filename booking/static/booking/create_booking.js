$(document).ready(function() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Handle form submission
    $('#booking-form').on('submit', function(e) {
        e.preventDefault();

        const bookingData = {
            customer_name: $('#customer_name').val(),
            sport_id: $('#sport_id').val(),
            booking_datetime: $('#booking_datetime').val(),
            duration: $('#duration').val()
        };

        console.log(bookingData);

        // Make an AJAX POST request to create a new booking
        $.ajax({
            url: '/booking/create/',
            method: 'POST',
            data: JSON.stringify(bookingData),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(data) {
                $('#total_price').text(`Rs. ${data.total_price}`);

                const newRow = `
                    <tr class="border-b bg-green-100 transition-all duration-1000 ease-in-out" id="new-booking-row">
                        <td class="px-4 py-3 text-sm text-gray-700">${data.customer_name}</td>
                        <td class="px-4 py-3 text-sm text-gray-700">${data.sport_name}</td>
                        <td class="px-4 py-3 text-sm text-gray-700">${data.booking_datetime}</td>
                        <td class="px-4 py-3 text-sm text-gray-700">${data.duration}</td>
                        <td class="px-4 py-3 text-sm text-gray-700"><b>$${data.total_price}</b></td>
                    </tr>
                `;
                
                $('tbody').prepend(newRow);

                setTimeout(function() {
                    $('#new-booking-row').removeClass('bg-green-100');
                }, 3000);
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });
});
