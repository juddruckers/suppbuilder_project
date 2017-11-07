function addItem(variation){
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});	
}

function removeItem(variation){
	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'variation': variation},
	})	
}

$(".product-add").on("click", function(){
	/*
	get the previous sibling which is a select bar
	*/
		var select = $(this).prev();
		var variation = select.val();
		var title = select.find(":selected").data("title");
		console.log(title);
	//disable the select bar after adding product
		select.attr("disabled", true);

	// make the checkmark show on the added product
		$('#caffeine-check').removeClass("hidden");

	// hide the button and show the remove product button
		$(this).hide();
		$(this).next().show();

	// add the item to the cart
		addItem(variation);

});

$(".product-remove").on("click", function(){
	// grab the previous sibling select
	var select = $(this).prevAll("select:first");
	var variation = select.val();
	//enable the select bar after removing product
	select.attr("disabled", false);

	// hide the checkmark because the item is remove

	// hide this button and show the product add button
	$(this).hide();
	$(this).prev().show();

	//add the item to the cart
	removeItem(variation) 

});

$(".product-select").change(function(){
	// on change the price of the product displayed should change

	// retrieve the price and the per serving cost from the selected option
	var selected = $(this).find(":selected"),
			price = selected.data("price"),
			serving = selected.data("serving");
			title = selected.data("title")

	// update the old price and old serving cost with the new option selected
	$("." + title + "-cost").text(price);
	$("." + title + "-serving-cost").text(serving);	

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




