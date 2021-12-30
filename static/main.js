
$(document).ready(function() {
const user_input = $("#search-input")
const partial_room_div = $('#partial-room')
const endpoint = ''
const delay_by_in_ms = 500
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            partial_room_div.fadeTo(500, 0).promise().then(() => {
                // replace the HTML contents
                partial_room_div.html(response['rooms'])
                // fade-in the div with new contents
                partial_room_div.fadeTo(500, 1)
                
            })
            
        })
}



user_input.on('keyup', function () {
    const request_parameters = {
        q: $(this).val() // value of user_input: the HTML element with ID user-input
    }

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
    
    }) 
})