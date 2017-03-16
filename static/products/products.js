


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
	var size = $('option:selected', this).attr('data-serving-size');
	$("#caffeine-size").text(size+ "/serving")
	$("#caffeine-price").text(" $" + option + " ($" + caffeine_price_per_serving + "/serving)")

})


$("#theanine-select").change(function(){
	console.log('change detected')
	var option = Number($('option:selected', this).attr('data-theanine-price'));
	var theanine_price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#theanine-size").text(size+ "/serving")
	$("#theanine-price").text("$ " + option + " ($" + theanine_price_per_serving + "/serving)")

})





