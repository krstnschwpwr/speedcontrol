$(document).ready(function () {
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
});
