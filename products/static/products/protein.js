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



$(".whey-add").on("click", function(added){

	var variation = $("#whey-select").val();

	console.log(variation)

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});

	$(this).hide();

	// disable the whey select
	$("#whey-select").attr('disabled', true);
	// collapse the select field
	$("#whey-options").collapse('hide');
	// show the whey remove button
	$(".whey-remove").show();
	// hide the whey description
	$('#whey-description').collapse('hide')

});


$(".whey-remove").on("click", function(){
	var product_id = $("#whey-select").val();
	
	console.log(product_id)
	$.ajax({
		url : '/shopping/delete/' ,
		type: 'POST',
		data:{'product_id' : product_id},
	})
	$(this).hide();

	// enable the product select
	$("#whey-select").attr("disabled", false);

	// uncollapse product option field if it is collapsed
	$("#whey-options").collapse('show');
	
	// show the product add button
	$(".whey-add").show();

	$('#whey-description').collapse('show')

});



$("#whey-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-whey-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#whey-size").text(size+ "/serving")
	$("#whey-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})









$(".caseine-add").on("click", function(added){

	var variation = $("#caseine-select").val();

	console.log(variation)

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});

	$(this).hide();

	// disable the whey select
	$("#caseine-select").attr('disabled', true);
	// collapse the select field
	$("#caseine-options").collapse('hide');
	// show the whey remove button
	$(".caseine-remove").show();
	// hide the whey description
	$('#caseine-description').collapse('hide')

});




$(".caseine-remove").on("click", function(){
	var product_id = $("#caseine-select").val();
	
	console.log(product_id)
	$.ajax({
		url : '/shopping/delete/' ,
		type: 'POST',
		data:{'product_id' : product_id},
	})
	$(this).hide();

	// enable the product select
	$("#caseine-select").attr("disabled", false);

	// uncollapse product option field if it is collapsed
	$("#caseine-options").collapse('show');
	
	// show the product add button
	$(".caseine-add").show();

	$('#caseine-description').collapse('show')

});



$("#caseine-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-caseine-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#caseine-size").text(size+ "/serving")
	$("#caseine-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})


$(".pea_protein-add").on("click", function(added){

	var variation = $("#pea_protein-select").val();

	console.log(variation)

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});

	$(this).hide();

	// disable the whey select
	$("#pea_protein-select").attr('disabled', true);
	// collapse the select field
	$("#pea_protein-options").collapse('hide');
	// show the whey remove button
	$(".pea_protein-remove").show();
	// hide the whey description
	$('#pea_protein-description').collapse('hide')

});




$(".pea_protein-remove").on("click", function(){
	var product_id = $("#pea_protein-select").val();
	
	console.log(product_id)
	$.ajax({
		url : '/shopping/delete/' ,
		type: 'POST',
		data:{'product_id' : product_id},
	})
	$(this).hide();

	// enable the product select
	$("#pea_protein-select").attr("disabled", false);

	// uncollapse product option field if it is collapsed
	$("#pea_protein-options").collapse('show');
	
	// show the product add button
	$(".pea_protein-add").show();

	$('#pea_protein-description').collapse('show')

});



$("#pea_protein-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-pea_protein-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#pea_protein-size").text(size+ "/serving")
	$("#pea_protein-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})

$(".soy_protein-add").on("click", function(added){

	var variation = $("#soy_protein-select").val();

	console.log(variation)

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});

	$(this).hide();

	// disable the whey select
	$("#soy_protein-select").attr('disabled', true);
	// collapse the select field
	$("#soy_protein-options").collapse('hide');
	// show the whey remove button
	$(".soy_protein-remove").show();
	// hide the whey description
	$('#soy_protein-description').collapse('hide')

});




$(".soy_protein-remove").on("click", function(){
	var product_id = $("#soy_protein-select").val();
	
	console.log(product_id)
	$.ajax({
		url : '/shopping/delete/' ,
		type: 'POST',
		data:{'product_id' : product_id},
	})
	$(this).hide();

	// enable the product select
	$("#soy_protein-select").attr("disabled", false);

	// uncollapse product option field if it is collapsed
	$("#soy_protein-options").collapse('show');
	
	// show the product add button
	$(".soy_protein-add").show();

	$('#soy_protein-description').collapse('show')

});



$("#soy_protein-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-soy_protein-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#soy_protein-size").text(size+ "/serving")
	$("#soy_protein-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})


