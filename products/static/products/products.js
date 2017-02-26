


$(".caffeine-add").on("click", function(added){

	var variation = $("#caffeine-select").val();

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});

	$(this).hide();

	$("#caffeine-select").attr('disabled', true);
	$(".caffeine-remove").show();

});



$(".caffeine-remove").on("click", function(){
	var product_id = $("#caffeine-select").val();
	$.ajax({
		url : '/shopping/delete/' ,
		type: 'POST',
		data:{'product_id' : product_id},
	})

	$("#caffeine-select").attr("disabled", false);
	$(this).hide();
	$(".caffeine-add").show();
});



$(".theanine-add").on("click", function(added){

	var variation = $("#theanine-select").val();

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});

	console.log("item added");

	$(this).hide();

	$("#theanine-select").attr('disabled', true);
	$(".theanine-remove").show();

});



$(".theanine-remove").on("click", function(){
	var product_id = $("#theanine-select").val();

	$.ajax({
		url : '/shopping/delete/',
		type: 'POST',
		data: {'product_id': product_id},
	})

	$("#theanine-select").attr("disabled", false);
	$(this).hide();
	$(".theanine-add").show();
});


$(document).ready(function() {


	
	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie !== '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) === (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');

	function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});


});

$("#caffeine-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-caffeine-price'));
	var caffeine_price_per_serving = (option / 30).toFixed(2);
	$("#caffeine-price").text(" $" + option + " ($" + caffeine_price_per_serving + "/serving)")

})


$("#theanine-select").change(function(){
	console.log('change detected')
	var theanine_selected = Number($("#theanine-select").val());
	var current_theanine_price = theanine_selected.toFixed(2);	
	var theanine_price_per_serving = (current_theanine_price / 30).toFixed(2);
	$("#theanine-price").text("$ " + current_theanine_price + " ($" + theanine_price_per_serving + "/serving)")

})





