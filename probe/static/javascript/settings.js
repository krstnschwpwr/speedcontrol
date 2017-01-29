$(document).ready(function () {
    $(function() {
    var xpathname = window.location.pathname;
    if (xpathname == '/settings') {
        $('body').addClass('unscroll settings');
    }
});

    $('.set').append('<div class="list">' + '<ul>' +
        '<li id="tit"><h4> LAST RECORD </h4></li>' +
        '<li id="up">UPLOAD: <span></span> </li>' +
        '<li id="down"> DOWNLOAD:<span></span> </li>' +
        '<li id="prtg_url"> PRTG URL:  <span></span> </li>' +
        '<li id="prtg_token"> PRTG TOKEN:<br><span></span> </li>'
        + '<li class="box"><a href="javascript:history.back()"><p> Take Me Back  ⇋</p></a></li>' +
        '</ul>'+ '</div>');


    const x = new mojs.Shape({
        className: 'circ',
        shape: 'circle',
        scale: {0: 3, easing: 'cubic.out'},
        stroke: {'#fc007b': '#6bf9ef', '#b3ff00': '#00fffe'},
        fill: 'transparent',
        origin: '100% 50%',
        angle: {[-50]: 100},
        right: '20%',
        radius: 50,
        duration: 800,
        repeat: 0,
        x: -100,
        easing: 'cubic.in',
    })
        .then({
            strokeWidth: 2,
            fill: '#fc007b',
            bottom: '60%',
            angle: 190,
            radius: 130,
            stroke: 'transparent',
            repeat: 0,
            scale: {to: 5, easing: 'sin.in'},
        }).play();


    $("#prtg_fields input").focusout(function () {
        var url = $('#url').val().trim();
        url = url.replace(/\/?$/, '/');
        $("#prtg_fields input[name='prtg_url']").val(url);

    });
    $('#prtg').change(function () {
        if ($('#prtg').is(':checked')) {
            $("#prtg_fields").fadeIn();
            $(".field:last-child").css("margin-top", "10% !important;")
        } else {
            $('#prtg_fields').fadeOut();
        }
    });
    $('.start.set .input-k').delay(1300).fadeIn(200);
    $('.prev a').delay(1300).fadeIn(200);


    loadUserRecord(function (d) {
        $('li#up span').text(d[0].expected_upload)
        $('li#down span').text(d[0].expected_download)
        console.log(d)
        $('li#prtg_url span').text(d[0].prtg_url)
        $('li#prtg_token span').text(d[0].prtg_token)

    });

    function loadUserRecord(cb) {
        if (cb) {
            $.ajax({
                url: '/api/v1/user-record',
                method: 'get',
                dataType: 'json'
            }).done(cb);


        }
    }




});


