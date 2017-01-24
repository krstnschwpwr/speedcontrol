$(document).ready(function () {
	$("#prtg_fields input").focusout(function () {
		var url = $('#url').val().trim();
		url = url.replace(/\/?$/, '/');
		$("#prtg_fields input[name='prtg_url']").val(url);

	});


	$(".title-wrapper").hide();
	$(".ui.fixed.borderless.menu").hide();
	$(".title-wrapper").delay(5100).fadeIn(200);
	$("form").delay(5000).fadeIn(200);
	$(".ui.fixed.borderless.menu").delay(5000).fadeIn(200);
	$(".logo").delay(5000).fadeOut(100);

	$('#prtg').change(function () {
		if ($('#prtg').is(':checked')) {
			$("#prtg_fields").fadeIn();
			$(".field:last-child").css("margin-top", "10% !important;")
		} else {
			$('#prtg_fields').fadeOut();
		}
	});
});
