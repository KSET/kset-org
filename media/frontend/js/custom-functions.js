
// define globals
var events_count;
var max_events = 6;
var current_event = 0;
var scrollViewport;
var scrollBar;

// on page load
$( function()
{
    // load calendar
    loadCalendar();

    // top menu open on click - mobile
    $('#top-menu').click(function() { $(this).toggleClass('open-menu'); });

    // header scroll expand on click - mobile
    $('#header-scroll').click(function() {
      $('#header-scroll').toggleClass('scroll-expanded');
    });
    $('#header-scroll a').click(function(event){
        event.stopPropagation();
    });

    var $topMenuPrompt = $('#top-menu-prompt');
    // top menu prompt blink
    window.setInterval(function(){
        $topMenuPrompt.toggleClass('prompt-blink');
    }, 500);

    events_count = $('#header-scroll .item').length;
    scrollViewport = jQuery('#header-scroll-viewport');
    scrollBar = jQuery('#header-scrollbar');

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

        if (( event.originalEvent.wheelDelta < 0 ) || (deltaY < 0)) {
            header_scroll_down();
            return false;
        } else {
            return header_scroll_up();
        }

    });
    // set scrollbar height
    $('#header-scrollbar').css('height', (max_events/events_count)*100+ '%');

    // FANCYBOX
    $("a[href$='.jpg'],a[href$='.png'],a[href$='.gif']").attr('rel', 'gallery').fancybox();
});


// functions


function GetCalendar(year, month)
{

  var selectedDate = document.location.pathname.match(/([0-9]{4})\-([0-9]{2})\-[0-9]{2}/);
  if ( (selectedDate) && (!year) && (!month) ) {
    year = selectedDate[1];
    month = selectedDate[2];
  } else if ((!year) && (!month)) {
    year = (new Date()).getFullYear();
    month = (new Date()).getMonth()+1;
  }

  $("#calendar").load("/kalendar/",{'year': year, 'month': month},function() {
    // mark selected date

    if (selectedDate) {
      $('.date-' + selectedDate[0]).addClass('current');
    }
  });
}

function loadCalendar() {
  GetCalendar();
}

function header_scroll_down()
{
    if (current_event < events_count - max_events) {
        scrollViewport.css({'top': (- (++current_event) * 48) });
        scrollBar.css('top', (current_event/(events_count))*100 + '%' );
        return false;
    }
}

function header_scroll_up()
{
    if (current_event > 0) {
        scrollViewport.css({'top': (- (--current_event) * 48)} );
        scrollBar.css('top', (current_event/(events_count))*100 + '%' );
        return false;
    }
}

function flip_element_by_id(id) {
    jQuery('#'+id).animate({height:'toggle'}, 300);
}



