// script.js

function sendClick(button_id) {
    $.ajax({
        type: "POST",
        url: "/click",
        data: { 'button_id': button_id },
        success: function(response) {
            if(response.status === 'success') {
                console.log('Click recorded');
            } else {
                console.error('Error:', response.message);
            }
        },
        error: function(error) {
            console.error('AJAX Error:', error);
        }
    });
}
