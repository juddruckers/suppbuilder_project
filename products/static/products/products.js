

$(".caffeine-add").on("click", function(added){

	var variation = $("#caffeine-select").val();

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});

	$(this).hide();
	
	$("#caffeine-select").attr('disabled', true);
	$(".caffeine-remove").show();
	$('#caffeineCollapse').collapse('hide')
	$('#selectCaffeine').collapse('hide')

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
	$('#caffeineCollapse').collapse('show');
	$('#selectCaffeine').collapse('show');
});


$("#caffeine-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-caffeine-price'));
	var caffeine_price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#caffeine-size").text(size+ "/serving")
	$("#caffeine-price").text(" $" + option + " ($" + caffeine_price_per_serving + "/serving)")

})

$(".theanine-add").on("click", function(added){

	var variation = $("#theanine-select").val();

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});



	$(this).hide();

	$("#theanine-select").attr('disabled', true);
	$(".theanine-remove").show();
	$('#theanineCollapse').collapse('hide')
	$('#selectTheanine').collapse('hide')

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
	$('#theanineCollapse').collapse('show');
	$('#selectTheanine').collapse('show');
});


$("#theanine-select").change(function(){
	console.log('change detected')
	var option = Number($('option:selected', this).attr('data-theanine-price'));
	var theanine_price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#theanine-size").text(size+ "/serving")
	$("#theanine-price").text("$ " + option + " ($" + theanine_price_per_serving + "/serving)")

})

$(".creatine-add").on("click", function(added){

	var variation = $("#creatine-select").val();

	console.log(variation)

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});

	$(this).hide();

	// disable the whey select
	$("#creatine-select").attr('disabled', true);
	// collapse the select field
	$("#creatine-options").collapse('hide');
	// show the whey remove button
	$(".creatine-remove").show();
	// hide the whey description
	$('#creatine-description').collapse('hide')

});




$(".creatine-remove").on("click", function(){
	var product_id = $("#creatine-select").val();
	
	console.log(product_id)
	$.ajax({
		url : '/shopping/delete/' ,
		type: 'POST',
		data:{'product_id' : product_id},
	})
	$(this).hide();

	// enable the product select
	$("#creatine-select").attr("disabled", false);

	// uncollapse product option field if it is collapsed
	$("#creatine-options").collapse('show');
	
	// show the product add button
	$(".creatine-add").show();

	$('#creatine-description').collapse('show')

});



$("#creatine-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-creatine-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#creatine-size").text(size+ "/serving")
	$("#creatine-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})

$(".beta_alanine-add").on("click", function(added){

	var variation = $("#beta_alanine-select").val();

	console.log(variation)

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});

	$(this).hide();

	// disable the whey select
	$("#beta_alanine-select").attr('disabled', true);
	// collapse the select field
	$("#beta_alanine-options").collapse('hide');
	// show the whey remove button
	$(".beta_alanine-remove").show();
	// hide the whey description
	$('#beta_alanine-description').collapse('hide')

});




$(".beta_alanine-remove").on("click", function(){
	var product_id = $("#beta_alanine-select").val();
	
	console.log(product_id)
	$.ajax({
		url : '/shopping/delete/' ,
		type: 'POST',
		data:{'product_id' : product_id},
	})
	$(this).hide();

	// enable the product select
	$("#beta_alanine-select").attr("disabled", false);

	// uncollapse product option field if it is collapsed
	$("#beta_alanine-options").collapse('show');
	
	// show the product add button
	$(".beta_alanine-add").show();

	$('#beta_alanine-description').collapse('show')

});



$("#beta_alanine-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-beta_alanine-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#beta_alanine-size").text(size+ "/serving")
	$("#beta_alanine-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})


$(".bcaa-add").on("click", function(added){

	var variation = $("#bcaa-select").val();

	console.log(variation)

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});

	$(this).hide();

	// disable the whey select
	$("#bcaa-select").attr('disabled', true);
	// collapse the select field
	$("#bcaa-options").collapse('hide');
	// show the whey remove button
	$(".bcaa-remove").show();
	// hide the whey description
	$('#bcaa-description').collapse('hide')

});




$(".bcaa-remove").on("click", function(){
	var product_id = $("#bcaa-select").val();
	
	console.log(product_id)
	$.ajax({
		url : '/shopping/delete/' ,
		type: 'POST',
		data:{'product_id' : product_id},
	})
	$(this).hide();

	// enable the product select
	$("#bcaa-select").attr("disabled", false);

	// uncollapse product option field if it is collapsed
	$("#bcaa-options").collapse('show');
	
	// show the product add button
	$(".bcaa-add").show();

	$('#bcaa-description').collapse('show')

});



$("#bcaa-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-bcaa-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#bcaa-size").text(size+ "/serving")
	$("#bcaa-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})


$(".citrulline_malate-add").on("click", function(added){

	var variation = $("#citrulline_malate-select").val();

	console.log(variation)

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});

	$(this).hide();

	// disable the whey select
	$("#citrulline_malate-select").attr('disabled', true);
	// collapse the select field
	$("#citrulline_malate-options").collapse('hide');
	// show the whey remove button
	$(".citrulline_malate-remove").show();
	// hide the whey description
	$('#citrulline_malate-description').collapse('hide')

});




$(".citrulline_malate-remove").on("click", function(){
	var product_id = $("#citrulline_malate-select").val();
	
	console.log(product_id)
	$.ajax({
		url : '/shopping/delete/' ,
		type: 'POST',
		data:{'product_id' : product_id},
	})
	$(this).hide();

	// enable the product select
	$("#citrulline_malate-select").attr("disabled", false);

	// uncollapse product option field if it is collapsed
	$("#citrulline_malate-options").collapse('show');
	
	// show the product add button
	$(".citrulline_malate-add").show();

	$('#citrulline_malate-description').collapse('show')

});



$("#citrulline_malate-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-citrulline_malate-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#citrulline_malate-size").text(size+ "/serving")
	$("#citrulline_malate-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})




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




