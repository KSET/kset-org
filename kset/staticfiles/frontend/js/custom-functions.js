/* globals $, Modernizr */
'use strict';

// define globals
var scrollViewport;

function supportsSvg() {
    return document.implementation.hasFeature("http://www.w3.org/TR/SVG11/feature#Image", "1.1");
}

// on page load
$( function()
{
    // load calendar
    loadCalendar();

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

    scrollViewport = $('#header-scroll-viewport');

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
    $(".ctrl-gallery-pic").magnificPopup({
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

    $('.open-form').click(function() {
        $(this).next('.form').slideToggle(200);
        return false;
    });

    if (!supportsSvg()) {
        $('#kset-logo').attr('src', '/static/frontend/images/kset_logo.png');
    }


    var staticThumbs = $('.news-item-0 .news-item-thumb, .news-item-1:last-child .news-item-thumb');

    var $win = $(window).scroll(function() {
        if ($win.width() < 650) return;
        staticThumbs.each(function() {
            var el = $(this);
            var h = el.height();
            var w = el.width() + 10;

            var parent = el.parent();
            var pt = parent.offset().top;
            var pb = parent.offset().top + parent.height();

            var st = $win.scrollTop();


            if (st + 10 < pt) {
                el.css({position: 'relative', top: 0});
            } else if (st + h > pb + 10) {
                el.css({position: 'relative', top: pb - h - pt});
            } else {
                el.css({position: 'fixed', top: 10, width: w});
            }


        });
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



