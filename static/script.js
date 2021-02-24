$(document).ready(function() {

	$(".message").css('visibility', 'hidden');
	$('select').selectpicker();


	$('#generate').on('submit', function(event) {
		$.ajax({
			data : {
				brand : $('#brand').val()
			},
			type : 'POST',
			url : '/generate'
		})

		.done(function(data) {
			$('#generatedNumber').text(data.number).css('visibility', 'visible');
		});
		event.preventDefault();
	});

	$('#validate').on('submit', function(event) {
		$.ajax({
			data : {
				number : $('#number').val()
			},
			type : 'POST',
			url : '/validate'
		})

		.done(function(data) {
			$('#validatedNumber').text(data.message).css('visibility', 'visible');;
		});
		event.preventDefault();
	});

	$('#advanced').on('submit', function(event) {
		$.ajax({
			data : {
				brand : $('#brand').val(),
				count : $('#count').val(),
				data_format : $('#data_format').val()
			},
			type : 'POST',
			url : '/adv_generator'
		})

		.done(function(data) {
			$('textarea').text(JSON.stringify(data.json, null, 2));
		});
		event.preventDefault();
	});
});