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


$('.update-cart').on("click", function(){
	// empty array to hold the ID's of items to be deleted
	var delete_item_list = []

	// select all checkboxes
	$(":checkbox").each(function(){
		// if the checkbox is checked push the cart item ID to delete_item_list
		if ($(this).is(":checked")) {
			delete_item_list.push($(this).val());
		};
	});

	// send the array of item ID's and reload the page on success
	$.ajax({
		url : '/shopping/cart/',
		type: 'POST',
		data: {'delete_item_list': delete_item_list},
		success: function(){
			console.log("success");
			location.reload();
		},
	});
});
 

/*
listens to all radio buttons. On click it retrieves the value
of the radio button which is the the ID of the address. Once the
address ID is retrieved it is sent to the AddressChangeView to 
update the selected address to be the default address used for orders.

args:
	id: ID of the address the user wants as the default.
*/
$("input:radio[name='address']").on("click", function(){
	id = $(this).val()

	$.ajax({
		url : '/shopping/change/',
		type: 'POST',
		data: {'id': id},
		success: function(){
			$("#success-alert").slideDown(500).delay(750).slideUp(1000);
		},
	});	
})

// function to delete address
$(".delete-link").on("click", function(){

	var pk = $(this).attr('value');
	$("#delete-address-id").val(pk)
	var test_pk = $("#delete-address-id").val()
});


$("#delete-address").on("click", function(){
	var pk = $("#delete-address-id").val()
	
	$.ajax({
		url : '/shopping/remove-checkout-address/',
		type: 'POST',
		data: {'pk': pk},
		success: function(data){
			location.reload();
		},
	});	
})

