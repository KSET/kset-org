
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

    // opera mini detection
    var isOperaMini = (navigator.userAgent.indexOf('Opera Mini') > -1)

    // user modernizr to check if device supports touch and is small (mobile)
    // adjust event names accordingly
    var touchend = 'touchend';
    var touchstart = 'touchstart';
    if ((!Modernizr.touch) && Modernizr.mq('(max-width: 650px)')) {
        touchend = (touchstart = 'click');
    }

    // top menu open on click - mobile
    $('#top-menu').on(touchend, function(e) {
        e.preventDefault();
        $('#top-menu').toggleClass('open-menu');
    });

    // header scroll expand on click - mobile
    $('#header-scroll-control').bind(touchstart, function(e) {
        e.preventDefault();
        var open = $('#header-scroll').toggleClass('scroll-expanded').hasClass('scroll-expanded');
        if (open) {
            $(this).html('-');
        } else {
            $(this).html('+');
        }
    });
    $('#top-menu a').bind(touchend, function(event){
        event.stopPropagation();
    });

    var $topMenuPrompt = $('#top-menu-prompt');
    // top menu prompt blink
    if (!isOperaMini) {
        setInterval(function(){
            $topMenuPrompt.toggleClass('prompt-blink');
        }, 500);
    }

    events_count = $('#header-scroll .item').length;
    scrollViewport = jQuery('#header-scroll-viewport');
    scrollBar = jQuery('#header-scrollbar');

    // bind events
    $('#newsletter-subscription').click(function () { $('#newsletter-subscription').val(''); });
    $('#newsletter-submit').click( function ()
       {
       $.post(
           "/subscribe/",
           { email: $('#newsletter-subscription').val()},
           function (data) {
           $('#newsletter-message').html(data);
           $('#newsletter-message').show();
           }
       );
    });
    // use enter key as well
    $('#form-newsletter').submit( function (event){
        $.post(
               "/subscribe/",
               { email: $('#newsletter-subscription').val()},
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

    // HAXORZ
    $(document).keypress(function(e){
        if (e.target.nodeName ==='INPUT') return;
        if (e.which == 106)
            header_scroll_down();
        else if (e.which == 107)
            header_scroll_up();
    });
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
        var viewportTop = (- (++current_event) * 48);
        var scrollbarTop = (current_event/events_count);
        if (Modernizr.csstransforms) {
            scrollViewport.css({ 'transform': 'translate3d(0,' + viewportTop+ 'px,0)' });
            scrollBar.css({ 'transform': 'translate(0,' + scrollbarTop*285 + 'px)' });
        } else {
            scrollViewport.css({ 'top': viewportTop });
            scrollBar.css({ 'top': scrollbarTop*100 + '%' });
        }
        return false;
    }
}

function header_scroll_up()
{
    if (current_event > 0) {
        var viewportTop = (- (--current_event) * 48);
        var scrollbarTop = (current_event/events_count);
        if (Modernizr.csstransforms) {
            scrollViewport.css({ 'transform': 'translate3d(0,' + viewportTop+ 'px,0)' });
            scrollBar.css({ 'transform': 'translate(0,' + scrollbarTop*285 + 'px)' });
        } else {
            scrollViewport.css({ 'top': viewportTop });
            scrollBar.css({ 'top': scrollbarTop*100 + '%' });
        }
        return false;
    }
}

function flip_element_by_id(id) {
    jQuery('#'+id).animate({height:'toggle'}, 300);
}



