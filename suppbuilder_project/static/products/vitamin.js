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


$(".vitamin_c-add").on("click", function(added){

	var variation = $("#vitamin_c-select").val();

	console.log(variation)

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});

	$(this).hide();

	// disable the whey select
	$("#vitamin_c-select").attr('disabled', true);
	// collapse the select field
	$("#vitamin_c-options").collapse('hide');
	// show the whey remove button
	$(".vitamin_c-remove").show();
	// hide the whey description
	$('#vitamin_c-description').collapse('hide')

});




$(".vitamin_c-remove").on("click", function(){
	var product_id = $("#vitamin_c-select").val();
	
	console.log(product_id)
	$.ajax({
		url : '/shopping/delete/' ,
		type: 'POST',
		data:{'product_id' : product_id},
	})
	$(this).hide();

	// enable the product select
	$("#vitamin_c-select").attr("disabled", false);

	// uncollapse product option field if it is collapsed
	$("#vitamin_c-options").collapse('show');
	
	// show the product add button
	$(".vitamin_c-add").show();

	$('#vitamin_c-description').collapse('show')

});

$("#vitamin_c-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-vitamin_c-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#vitamin_c-size").text(size+ "/serving")
	$("#vitamin_c-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})


$(".vitamin_d-add").on("click", function(added){

	var variation = $("#vitamin_d-select").val();

	console.log(variation)

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});

	$(this).hide();

	// disable the whey select
	$("#vitamin_d-select").attr('disabled', true);
	// collapse the select field
	$("#vitamin_d-options").collapse('hide');
	// show the whey remove button
	$(".vitamin_d-remove").show();
	// hide the whey description
	$('#vitamin_d-description').collapse('hide')

});




$(".vitamin_d-remove").on("click", function(){
	var product_id = $("#vitamin_d-select").val();
	
	console.log(product_id)
	$.ajax({
		url : '/shopping/delete/' ,
		type: 'POST',
		data:{'product_id' : product_id},
	})
	$(this).hide();

	// enable the product select
	$("#vitamin_d-select").attr("disabled", false);

	// uncollapse product option field if it is collapsed
	$("#vitamin_d-options").collapse('show');
	
	// show the product add button
	$(".vitamin_d-add").show();

	$('#vitamin_d-description').collapse('show')

});



$("#vitamin_d-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-vitamin_d-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#vitamin_d-size").text(size+ "/serving")
	$("#vitamin_d-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})


$(".fish_oil-add").on("click", function(added){

	var variation = $("#fish_oil-select").val();

	console.log(variation)

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});

	$(this).hide();

	// disable the whey select
	$("#fish_oil-select").attr('disabled', true);
	// collapse the select field
	$("#fish_oil-options").collapse('hide');
	// show the whey remove button
	$(".fish_oil-remove").show();
	// hide the whey description
	$('#fish_oil-description').collapse('hide')

});




$(".fish_oil-remove").on("click", function(){
	var product_id = $("#fish_oil-select").val();
	
	console.log(product_id)
	$.ajax({
		url : '/shopping/delete/' ,
		type: 'POST',
		data:{'product_id' : product_id},
	})
	$(this).hide();

	// enable the product select
	$("#fish_oil-select").attr("disabled", false);

	// uncollapse product option field if it is collapsed
	$("#fish_oil-options").collapse('show');
	
	// show the product add button
	$(".fish_oil-add").show();

	$('#fish_oil-description').collapse('show')

});



$("#fish_oil-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-fish_oil-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#fish_oil-size").text(size+ "/serving")
	$("#fish_oil-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})

$(".glucosamine-add").on("click", function(added){

	var variation = $("#glucosamine-select").val();

	console.log(variation)

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});

	$(this).hide();

	// disable the whey select
	$("#glucosamine-select").attr('disabled', true);
	// collapse the select field
	$("#glucosamine-options").collapse('hide');
	// show the whey remove button
	$(".glucosamine-remove").show();
	// hide the whey description
	$('#glucosamine-description').collapse('hide')

});




$(".glucosamine-remove").on("click", function(){
	var product_id = $("#glucosamine-select").val();
	
	console.log(product_id)
	$.ajax({
		url : '/shopping/delete/' ,
		type: 'POST',
		data:{'product_id' : product_id},
	})
	$(this).hide();

	// enable the product select
	$("#glucosamine-select").attr("disabled", false);

	// uncollapse product option field if it is collapsed
	$("#glucosamine-options").collapse('show');
	
	// show the product add button
	$(".glucosamine-add").show();

	$('#glucosamine-description').collapse('show')

});



$("#glucosamine-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-glucosamine-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#glucosamine-size").text(size+ "/serving")
	$("#glucosamine-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})

