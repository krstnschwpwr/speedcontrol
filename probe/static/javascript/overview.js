  $(document).ready(function () {
            $('table').tablesort();
            $('#data .header').scrollToFixed();
            var back_to_top_button = ['<a href="#top" class="back-to-top">Top &#8657</a>'].join("");
            $("body").append(back_to_top_button)
            $(".back-to-top").hide();
            $(function () {
                $(window).scroll(function () {
                    if ($(this).scrollTop() > 100) { // Wenn 100 Pixel gescrolled wurde
                        $('.back-to-top').fadeIn();
                        $('.search.icon').css("color", "#12002c");
                        $('.box.center.dash.menu').hide();
                    } else {
                        $('.back-to-top').fadeOut();
                        $('.box.center.dash.menu').show();
                        $('.search.icon').css("color", "#ffffff");
                    }
                });
                $('.back-to-top').click(function () {
                    $('.box.center.dash.menu').show();
                    $('.search.icon').css("color", "#ffffff");
                    $('table').hide();
                    $('body,html').animate({
                        scrollTop: 0
                    }, 800);
                    return false;
                });
            });
        });
        function toggleTable() {
            var elem = document.getElementById("data");
            var hide = elem.style.display == "none";
            if (hide) {
                elem.style.display = "table";
                $('.box.center.dash.menu').hide();
            } else {
                elem.style.display = "none";
            }
        }


        function formatDate(d) {
            var date = new Date(d);
            var day = date.getDate();
            var monthIndex = date.getMonth() + 1;
            var year = date.getFullYear();
            return day + '.' + monthIndex + '.' + year;
        }
        $(document).ready(function () {
            $('.ui.search').search({
                apiSettings: {
                    url: '/search?query={query}'
                }
            });
        });


        var data = [];
        $(document).ready(function () {
            loadData(function (jsonData) {
                $.each(jsonData, function (index, item) {
                    data.push([formatDate(item.time), item.upload, item.download]);
                });
                google.charts.load('current', {'packages': ['corechart']});
                google.charts.setOnLoadCallback(drawChart);
            });
            loadData(function (d) {
                d.forEach(function (o) {
                    $('#data tbody').append(
                            '<tr>' +
                            '<td>' + formatDate(o.time) + '</td>' +
                            '<td>' + o.server + '</td>' +
                            '<td>' + o.ping + '&nbsp;ms</td>' +
                            '<td>' + f(o.download).val + '&nbsp;' + f(o.download).unit + '</td>' +
                            '<td>' + f(o.upload).val + '&nbsp;' + f(o.upload).unit + '</td>' +
                            '</tr>');
                });
            });
        });
        function drawChart() {
            var d = new google.visualization.DataTable(data);
            d.addColumn('string', 'Time');
            //d.addColumn('number', 'Ping');
            d.addColumn('number', 'Upload');
            d.addColumn('number', 'Download');
            d.addRows(data);
            var options = {
                legend: 'right',
                width: 1200,
                height: 600,
                colors: [ '#b3ff00', '#fc007b'] //'#6bd0ef',
            };
            // Instantiate and draw our chart, passing in some options.
            var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
            chart.draw(d, options);
            $('#chart .dimmer').dimmer('toggle');
        }
        function loadData(cb) {
            if (cb) {
                $.ajax({
                    url: '/api/v1/measurements',
                    method: 'get',
                    dataType: 'json'
                }).done(cb);
            }
        }
        function f(v) {
            units = ['bit/s', 'Kbit/s', 'Mbit/s', 'Gbit/s'];
            unit = 0;
            while (v >= 1024) {
                v /= 1024.0;
                unit += 1;
            }
            return {val: (v).toPrecision(2), unit: units[unit]};
        }