
// define globals
var events_count;
var max_events = 6;
var current_event = 0;


// on page load
$( function()
{
    // top menu prompt blink
    window.setInterval(function(){
        $('#top-menu-prompt').toggleClass('prompt-blink');
    }, 500);

    events_count = $('#header-scroll > div').length;

    // bind events
    $('#newsletter-subscription').click(function () { $('#newsletter-subscription').val(''); });
    $('#newsletter-submit').click( function ()
       {
       $.post(
           "/subscribe/",
           { subscription: $('#newsletter-subscription').val()},
           function (data) {
           $('#newsletter-message').html(data);
           $('#newsletter-message').show();
           }
       );
    });
    // da enter bude isto sto i ok
    $('#form-newsletter').submit( function (event){
        $.post(
               "/subscribe/",
               { subscription: $('#newsletter-subscription').val()},
               function (data) {
               $('#newsletter-message').html(data);
               $('#newsletter-message').show();
               }
           );
        event.preventDefault();
    });

    // header scroll
    $('#header-scroll').bind('mousewheel', function(event, delta, deltaX, deltaY) {

        if ( event.originalEvent.wheelDelta < 0 ) {
            return header_scroll_down();
        } else {
            return header_scroll_up();
        }

    });

});


// functions
function header_scroll_down()
{
    if (current_event < events_count - max_events) {
        jQuery('#event-' + current_event++).stop().slideUp(150);  // .animate({opacity:0},100).animate({height:'toggle'},100);
        return false;
    }
}

function header_scroll_up()
{
    if (current_event > 0) {
        jQuery('#event-' + --current_event).slideDown(150); // .animate({height:'toggle'},100).animate({opacity:100},100);
        return false;
    }
}

function flip_element_by_id(id) {
    jQuery('#'+id).animate({height:'toggle'}, 300);
}



