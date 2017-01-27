var initialized = false;


$(document).ready(function () {
	poll()
});


function l(d) {

	if (!initialized) {
		$('.ping.circle').circleProgress({value: d.ping, fill: {gradient: ["#340BE8", "#00fffe"]}});
		$('.upload.circle').circleProgress({
			value: (d.upload / max_up),
			fill: {gradient: ["#f84526", "#b3ff00"]}
		});
		$('.download.circle').circleProgress({
			value: (d.download / max_down),
			fill: {gradient: ["#A30CFF", "#fc007b"]}
		});
		initialized = true;
	} else {
		$('.ping.circle').circleProgress('value', d.ping);
		$('.upload.circle').circleProgress('value', (d.upload / max_up));
		$('.download.circle').circleProgress('value', (d.download / max_down));
	}
	$('.ping.circle strong').text(d.ping);
	$('.ping.circle .cen').text("ms");
	o = f(d.download);
	$('.download.circle strong').text(o.val);
	$('.download.circle .cen').text(o.unit);
	o = f(d.upload);
	$('.upload.circle strong').text(o.val);
	$('.upload.circle .cen').text(o.unit);
	$('#server').html(d.server);
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

function loadData(cb) {
	if (cb) {
		$.ajax({
			url: '/api/v1/measurements/latest',
			method: 'get',
			dataType: 'json'
		}).done(function (data) {
			if (data.status && data.status == 500) {
				data = {
					download: 0,
					server: "There are no measurements right now <i class='blind icon'></i>",
					upload: 0,
					ping: 0
				}
			}
			cb(data)
		});
	}
}

function loadQoS(cb) {
	if (cb) {
		$.ajax({
			url: '/api/v1/qualityofservice/latest',
			method: 'get',
			dataType: 'json'
		}).done(function (d) {
			if (d.length == 0) {
				d = {percentage: 0}
			}
			cb(d)
		});
	}
}

function poll() {

	loadData(l);

	loadQoS(function (d) {
		$('#q span').text(" " + d.percentage.toFixed(2) + "%");
	});

	window.setTimeout(poll, 5000);
}