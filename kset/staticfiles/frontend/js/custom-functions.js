
// define globals
var scrollViewport;

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

    scrollViewport = jQuery('#header-scroll-viewport');

    // bind events
    $('#newsletter-subscription').click(function () { $('#newsletter-subscription').val(''); });
    $('#newsletter-submit').click( function ()
       {
       $.post(
           "/subscribe/",
           { email: $('#newsletter-subscription').val()},
           function (data) {
             $('#newsletter-subscription').val(''); // clear form
             $('#newsletter-message').html(data);
             $('#newsletter-message').show();
           }
       ).fail(function(data) {
                $('#newsletter-message').html(data.responseText);
                $('#newsletter-message').show();
        });
    });
    // use enter key as well
    $('#form-newsletter').submit( function (event){
        $.post(
               "/subscribe/",
               { email: $('#newsletter-subscription').val()},
               function (data) {
                 $('#newsletter-subscription').val(''); // clear form
                 $('#newsletter-message').html(data);
                 $('#newsletter-message').show();
               }
           ).fail(function(data) {
                 $('#newsletter-message').html(data.responseText);
                 $('#newsletter-message').show();
           });
        event.preventDefault();
    });

    // header scroll
    var $headerScroll = $('#header-scroll');
    if ($(window).width() >= 650) {
        $headerScroll.perfectScrollbar({ wheelSpeed: 30 });
    }

    // GALLERY POPUP
    $("a[href$='.jpg'],a[href$='.png'],a[href$='.gif']").attr('rel', 'gallery').magnificPopup({
        type: 'image',
        gallery: {
            enabled: true,
            preload: [1, 2]
        }
    });

    // HAXORZ
    $(document).keypress(function(e){
        if (e.target.nodeName ==='INPUT') return;
        if (e.which == 106)
            $headerScroll.animate({scrollTop: $headerScroll.scrollTop() + 48}, 120);
        else if (e.which == 107)
            $headerScroll.animate({scrollTop: $headerScroll.scrollTop() - 48}, 120);
    });

    $('.club-right a[href*=mailto]').attr('href', function(i, href) {
        return href.replace('!at!', '@');
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
  scrollViewport.scrollTop(48);
  return false;
}

function header_scroll_up()
{
    scrollViewport.scrollTop(48);
    return false;
}

function flip_element_by_id(id) {
    jQuery('#'+id).slideToggle(300);
}



