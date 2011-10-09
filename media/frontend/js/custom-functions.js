
// define globals
var events_count;
var max_events = 6;
var current_event = 0;

// 

// on page load
jQuery(document).ready( function()
    {
	// top menu prompt blink
	window.setInterval(function(){
	    jQuery('#top-menu-prompt').toggleClass('prompt-blink');
	}, 500);
	
	events_count = jQuery('#header-scroll > div').length;
	
	// bind events
	jQuery('#newsletter-subscription').click(function () { $('#newsletter-subscription').val(''); });
	jQuery('#newsletter-submit').click( function () 
				       { 
					   jQuery.post(
					       "/subscribe/",
					       { subscription: jQuery('#newsletter-subscription').val()},
					       function (data) { 
						   jQuery('#newsletter-message').html(data);
						   jQuery('#newsletter-message').show();
					       }
					   ); 
				       });
	// da enter bude isto sto i ok
        jQuery('#form-newsletter').submit( function (event){
					jQuery.post(
					       "/subscribe/",
					       { subscription: jQuery('#newsletter-subscription').val()},
					       function (data) { 
						   jQuery('#newsletter-message').html(data);
						   jQuery('#newsletter-message').show();
					       }
					   ); 
					event.preventDefault();
	});
	
    });


// functions 
function header_scroll_down()
{
    if (current_event < events_count - max_events)
	jQuery('#event-' + current_event++).animate({opacity:0},200).animate({height:'toggle'},300);
}

function header_scroll_up()
{
    if (current_event > 0)
	jQuery('#event-' + --current_event).animate({height:'toggle'},300).animate({opacity:100},200);
}

function flip_element_by_id(id) {
    jQuery('#'+id).animate({height:'toggle'}, 300);
};



