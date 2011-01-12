
// define globals
var events_count;
var max_events = 6;
var current_event = 0;

// 

// on page load
$(document).ready( function()
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
	
    });


// functions 
function header_scroll_down()
{
    if (current_event < events_count - max_events)
	$('#event-' + current_event++).animate({opacity:0},200).animate({height:'toggle'},300);
}

function header_scroll_up()
{
    if (current_event > 0)
	$('#event-' + --current_event).animate({height:'toggle'},300).animate({opacity:100},200);
}

function flip_element_by_id(id) {
    $('#'+id).animate({height:'toggle'}, 300);
};



