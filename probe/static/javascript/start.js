
$(document).ready(function () {
     $(function () {
        var kk = window.location.pathname;
         console.log(kk);
        if (kk == '/start') {
            $('body').addClass('start');
        }
    });


    const cross = new mojs.Shape({
        className: 'circ',
        shape: 'circle',
        scale: {0: 4, easing: 'cubic.out'},
        stroke: {'#fc007b': '#6bf9ef', '#b3ff00': '#00fffe'},
        fill: 'transparent',
        origin: '100% 50%',
        angle: {[-180]: 180},
        left: '20%',
        radius: 50,
        duration: 2000,
        repeat: 0,
        y: -100,
        easing: 'cubic.in',
    })
        .then({
            strokeWidth: 2,
            fill: '#fc007b',
            top: '60%',
            angle: -20,
            radius: 130,
            stroke: 'transparent',
            repeat: 0,
            scale: {to: 5, easing: 'sin.in'},
        }).play();

    $(function () {
        var xpathname = window.location.pathname;
        if (xpathname == '/settings') {
            $('body').addClass('unscroll');
        }
    });
    $(".menu-circ").delay(3000).fadeIn(200);
    $(".logo").delay(2100).fadeIn(100);
    $('a').click(function () {
        $('.circ').fadeOut();
        $('.line').fadeOut();
        $('.line2').fadeOut();
    });
});