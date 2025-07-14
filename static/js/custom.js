(function( $ ) {
    'use strict';

    /*-----------------------------------
    One Page Nav
    -----------------------------------*/
    if ($('#one-page-nav').length > 0) {
        $('#one-page-nav').onePageNav({
            currentClass: 'active',
            filter: ':not(#search-toggle):not(.pages)'
        });
    }

    /*-----------------------------------
    Header Search Toggle 
    -----------------------------------*/
    $('#search-toggle, #search-toggle-mobile').on('click', function (st) {
        st.preventDefault();
        $('#header-search').slideToggle();
        $(this).children('.fa').toggleClass('fa-search fa-close');
    });

    /*-----------------------------------
    Mobile Navigation
    -----------------------------------*/
    function mobileNav() {
        $('.navbar-nav .dropdown').unbind('click');
        if ($(window).width() < 992) {
            $('.navbar-toggle').slideDown();
            $('.navbar-collapse').slideUp();

            $('body').on('click', function (e) {
                if ($('.navbar-collapse').is(':visible') && $('.navbar-toggle').is(':visible') && !$(e.target).is(".dropdown")) {
                    $('.navbar-collapse').collapse('hide');
                }
            });

            $('.navbar-nav .dropdown').on('click', function () {
                $(this).children('.dropdown-menu').slideToggle();
                $(this).toggleClass('submenu-opened');
            });
        } else {
            $('.navbar-toggle').slideUp();
            $('.navbar-collapse').slideDown();
        }
    }

    mobileNav();


    /*-----------------------------------
    Banner Carousel 
    -----------------------------------*/
    $('#banner-slider').owlCarousel({
        singleItem: true,
        slideSpeed: 200,
        //autoPlay: 3000,
        stopOnHover: true,
        navigation: true,
        navigationText: ['<i class=\"fa fa-angle-left\"><i>', '<i class=\"fa fa-angle-right\"><i>'],
        pagination: true,
    });

    /*-----------------------------------
    CountTo 
    -----------------------------------*/
    function animateCountTo(ct) {
        if ($.fn.visible && $(ct).visible() && !$(ct).hasClass('animated')) {
            $(ct).countTo({
                speed: 2000
            });
            $(ct).addClass('animated');
        }
    }

    function initCountTo() {
        var counter = $('.count');
        counter.each(function () {
            animateCountTo(this);
        });
    }

    initCountTo();

    /*-----------------------------------
    Countdown
    -----------------------------------*/
    $('.countdown-time').each(function () {
        var endTime = $(this).data('time');
        $(this).countdown(endTime, function (tm) {
            $(this).html(tm.strftime('<span class="section_count"><span class="tcount days">%D </span><span class="text">Dias</span></span><span class="section_count"><span class="tcount hours">%H</span><span class="text">Horas</span></span><span class="section_count"><span class="tcount minutes">%M</span><span class="text">Min</span></span><span class="section_count"><span class="tcount seconds">%S</span><span class="text">Seg</span></span>'));
        });
    });

    /*-----------------------------------
    Commingsoon Height
    -----------------------------------*/
    function commingsoonHeight() {
        if ($('#commingsoon-wrap').length > 0) {
            $('#commingsoon-wrap').css('height', $(window).height());
        }
    }

    commingsoonHeight();

    /*-----------------------------------
    Contact Form
    -----------------------------------*/
    // Function for email address validation
    function isValidEmail(emailAddress) {
        var pattern = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);

        return pattern.test(emailAddress);

    }
    $("#contactForm").on('submit', function (e) {
        e.preventDefault();
        var data = {
            name: $("#name").val(),
            email: $("#email").val(),
            fone: $("#fone").val(),
            message: $("#message").val()
        };

        if (isValidEmail(data['email']) && (data['message'].length > 1) && (data['name'].length > 1)) {
            $.ajax({
                type: "POST",
                url: base_url+"campanha/sendContatoAjax",
                data: data,
                success: function (resultData) {
                    $('#contactForm .input-success').delay(500).fadeIn(1000);
                    $('#contactForm .input-error').fadeOut(500);
                }
            });
        } else {
            $('#contactForm .input-error').delay(500).fadeIn(1000);
            $('#contactForm .input-success').fadeOut(500);
        }

        return false;
    });

   
    /*-----------------------------------
    Magnific Popup
    -----------------------------------*/
    $('.image-large').magnificPopup({
        type: 'image',
        gallery: {
            enabled: true
        }
    });
    $('.play-video').magnificPopup({
        type: 'iframe'
    });
    $.extend(true, $.magnificPopup.defaults, {
        iframe: {
            patterns: {
                youtube: {
                    index: 'youtube.com/',
                    id: 'v=',
                    src: 'https://www.youtube.com/embed/%id%?autoplay=1'
                }
            }
        }
    });

    /*-----------------------------------
    Testimonial Carousel
    -----------------------------------*/
    $('.testimonials-for').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: '.testimonial-nav',
        autoplay: true,
    });
    $('.testimonial-nav').slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        asNavFor: '.testimonials-for',
        dots: false,
        centerMode: true,
        focusOnSelect: true,
        prevArrow: '<button class=\"slick-prev\"><i class=\"fa fa-angle-left\"></i></button>',
        nextArrow: '<button class=\"slick-next\"><i class=\"fa fa-angle-right\"></i></button>',
        responsive: [
            {
                breakpoint: 991,
                settings: {
                    slidesToShow: 3
                }
			},
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1
                }
			}
		]
    });

    /*-----------------------------------
    Case Filter
    -----------------------------------*/
    if ($.fn.imagesLoaded && $('#cases').length > 0) {
        var $grid = $('#cases').isotope({
            itemSelector: '.grid-item',
        });

        $('.case-filter').on('click', 'button', function () {
            var filterValue = $(this).attr('data-filter');
            $grid.isotope({
                filter: filterValue
            });
            $('.case-filter button').removeClass('active');
            $(this).addClass('active');
        });
    }

    /*-----------------------------------
    Result chart
    -----------------------------------*/
    if ($('#result-chart').length > 0) {
        var ctx = $('#result-chart');
        var dataValue = ctx.data('value');
        var dataBg = ctx.data('bg');
        var dataLabel = ctx.data('label');

        var resultChart = new Chart(ctx, {
            type: 'polarArea',
            data: {
                datasets: [{
                    data: dataValue,
                    backgroundColor: dataBg,
                    label: 'My dataset' // for legend
            }],
                labels: dataLabel
            },
            options: {
                responsive: true,
                legend: {
                    position: 'bottom',
                },
                scale: {
                    ticks: {
                        beginAtZero: true
                    },
                    reverse: false
                },
                animation: {
                    animateRotate: true,
                    animateScale: true
                }
            }
        });
    }

    /*-----------------------------------
    Progess Bar
    -----------------------------------*/
    function animateProgressBar(pb) {
        if ($.fn.visible && $(pb).visible() && !$(pb).hasClass('animated')) {
            $(pb).css('width', $(pb).attr('aria-valuenow') + '%');
            $(pb).addClass('animated');
        }
    }

    function initProgressBar() {
        var progressBar = $('.progress-bar');
        progressBar.each(function () {
            animateProgressBar(this);
        });
    }

    initProgressBar();

    /*-----------------------------------
    Go to top
    -----------------------------------*/
    $('.scrollup').on('click',function () {
        $("html, body").animate({
            scrollTop: 0
        }, 600);
        return false;
    });


    /*-----------------------------------
    Window Scroll
    -----------------------------------*/
    $(window).on('scroll', function () {
        initCountTo();
        initProgressBar();

        if ($(this).scrollTop() > 100) {
            $('.scrollup').fadeIn();
        } else {
            $('.scrollup').fadeOut();
        }
    });

    $(window).on('resize orientationchange', function () {
        mobileNav();
        commingsoonHeight();
    });

})(jQuery);

$(window).on('load', function () {
    $("#preloader-wrap").delay(200).fadeOut();
    FormWizard.init();
});
