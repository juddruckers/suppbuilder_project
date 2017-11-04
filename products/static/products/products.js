function addItem(variation){
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});	
}

function removeItem(product_id){
	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})	
}

$(".product-add").on("click", function(){
	/*
	get the previous sibling which is a select bar
	*/
		var select = $(this).prev();
		var value = select.val();

	//disable the select bar after adding product
		select.attr("disabled", true);

	// make the checkmark show on the added product
		$('#caffeine-check').removeClass("hidden");

	// hide the button and show the remove product button
		$(this).hide();
		$(this).next().show();

	// add the item to the cart

	addItem(value)

});

$(".product-remove").on("click", function(){

})

// $(".caffeine-add").on("click", function(){

// 	var variation = $("#caffeine-select").val();
// 	var item_added = $("#caffeine-select option:selected").text();

// 	$(".modal-body").html("<p>" + item_added + " added to stack!</p>")
// 	addItem(variation);

// 	$(this).hide();
	
// 	$("#caffeine-select").attr('disabled', true);
// 	$(".caffeine-remove").show();
// 	$('#caffeineCollapse').collapse('hide')
// 	$('#selectCaffeine').collapse('hide')
// 	$('#caffeine-check').removeClass('hidden')

// });


$(".caffeine-remove").on("click", function(){
	var product_id = $("#caffeine-select").val();

	removeItem(product_id);

	$("#caffeine-select").attr("disabled", false);
	$(this).hide();
	$(".caffeine-add").show();
	$('#caffeineCollapse').collapse('show');
	$('#selectCaffeine').collapse('show');
	$('#caffeine-check').addClass('hidden')

});


$("#caffeine-select").change(function(){
	var option = Number($('option:selected', this).attr('data-caffeine-price'));
	var caffeine_price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#caffeine-size").text(size+ "/serving")
	$("#caffeine-price").text(" $" + option + " ($" + caffeine_price_per_serving + "/serving)")

})


$(".theanine-add").on("click", function(added){

	var variation = $("#theanine-select").val();

	
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});

	$(this).hide();

	$("#theanine-select").attr('disabled', true);
	$(".theanine-remove").show();
	$('#selectTheanine').collapse('hide');
	$('#theanine-check').removeClass('hidden');
});


$(".theanine-remove").on("click", function(){
	var product_id = $("#theanine-select").val();

	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})

	$("#theanine-select").attr("disabled", false);
	$(this).hide();
	$(".theanine-add").show();
	$('#selectTheanine').collapse('show');
	$('#theanine-check').addClass('hidden');
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

	
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});

	$(this).hide();

	$("#creatine-select").attr('disabled', true);
	$("#creatine-options").collapse('hide');
	$(".creatine-remove").show();
	$('#creatine-check').removeClass('hidden')
});



$(".creatine-remove").on("click", function(){
	var product_id = $("#creatine-select").val();
	

	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})
	$(this).hide();


	$("#creatine-select").attr("disabled", false);
	$("#creatine-options").collapse('show');
	$(".creatine-add").show();
	$('#creatine-check').addClass('hidden')
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
	
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});
	$(this).hide();

	$("#beta_alanine-select").attr('disabled', true);
	$("#beta_alanine-options").collapse('hide');
	$(".beta_alanine-remove").show();
	$('#beta-alanine-check').removeClass('hidden');
});


$(".beta_alanine-remove").on("click", function(){
	var product_id = $("#beta_alanine-select").val();
	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})
	$(this).hide();

	$("#beta_alanine-select").attr("disabled", false);
	$("#beta_alanine-options").collapse('show');
	$(".beta_alanine-add").show();
	$('#beta-alanine-check').addClass('hidden');
});


$("#beta_alanine-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-beta_alanine-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#beta_alanine-size").text(size+ "/serving")
	$("#beta_alanine-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})

$("#beta_alanine-select-2").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-beta_alanine-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#beta_alanine-size-2").text(size+ "/serving")
	$("#beta_alanine-price-2").text(" $" + option + " ($" + price_per_serving + "/serving)")
})



$(".bcaa-add").on("click", function(added){

	var variation = $("#bcaa-select").val();
	
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});
	$(this).hide();

	$("#bcaa-select").attr('disabled', true);
	$("#bcaa-options").collapse('hide');
	$(".bcaa-remove").show();

	$('#bcaa-check').removeClass('hidden');

});



$(".bcaa-remove").on("click", function(){
	var product_id = $("#bcaa-select").val();
	
	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})
	$(this).hide();

	$("#bcaa-select").attr("disabled", false);
	$("#bcaa-options").collapse('show');
	$(".bcaa-add").show();
	$("#bcaa-check").addClass('hidden');
});

$("#bcaa-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-bcaa-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#bcaa-size").text(size+ "/serving");
	$("#bcaa-price").text(" $" + option + " ($" + price_per_serving + "/serving)");

})

$(".citrulline_malate-add").on("click", function(added){

	var variation = $("#citrulline_malate-select").val();
	
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});

	$(this).hide();

	$("#citrulline_malate-select").attr('disabled', true);
	$("#citrulline_malate-options").collapse('hide');
	$(".citrulline_malate-remove").show();
	$("#citrulline-malate-check").removeClass('hidden');

});

$(".citrulline_malate-remove").on("click", function(){
	var product_id = $("#citrulline_malate-select").val();

	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})
	$(this).hide();

	$("#citrulline_malate-select").attr("disabled", false);
	$("#citrulline_malate-options").collapse('show');
	$(".citrulline_malate-add").show();
	$('#citrulline-malate-check').addClass('hidden');
});

$("#citrulline_malate-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-citrulline_malate-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#citrulline_malate-size").text(size+ "/serving")
	$("#citrulline_malate-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})

$(".glutamine-add").on("click", function(added){

	var variation = $("#glutamine-select").val();

	
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});

	$(this).hide();

	$("#glutamine-select").attr('disabled', true);
	$("#glutamine-options").collapse('hide');
	$(".glutamine-remove").show();
	$('#glutamine-check').removeClass('hidden');
});

$(".glutamine-remove").on("click", function(){
	var product_id = $("#glutamine-select").val();
	
	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})
	$(this).hide();

	$("#glutamine-select").attr("disabled", false);
	$("#glutamine-options").collapse('show');
	$(".glutamine-add").show();
	$('#glutamine-check').addClass('hidden');

});

$("#glutamine-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-glutamine-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#glutamine-size").text(size+ "/serving")
	$("#glutamine-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})

$(".acetyl_l_carnitine-add").on("click", function(added){

	var variation = $("#acetyl_l_carnitine-select").val();


	
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});

	$(this).hide();

	$("#acetyl_l_carnitine-select").attr('disabled', true);
	$("#acetyl_l_carnitine-options").collapse('hide');
	$(".acetyl_l_carnitine-remove").show();
	$('#acetyl_l_carnitine-check').removeClass('hidden');
});

$(".acetyl_l_carnitine-remove").on("click", function(){
	var product_id = $("#acetyl_l_carnitine-select").val();
	
	
	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})
	$(this).hide();

	$("#acetyl_l_carnitine-select").attr("disabled", false);
	$("#acetyl_l_carnitine-options").collapse('show');
	$(".acetyl_l_carnitine-add").show();
	$('#acetyl_l_carnitine-check').addClass('hidden');

});

$("#acetyl_l_carnitine-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-acetyl_l_carnitine-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#acetyl_l_carnitine-size").text(size+ "/serving")
	$("#acetyl_l_carnitine-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})

$(".ornithine-add").on("click", function(added){

	var variation = $("#ornithine-select").val();

	
	
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});

	$(this).hide();

	$("#ornithine-select").attr('disabled', true);
	$("#ornithine-options").collapse('hide');
	$(".ornithine-remove").show();
	$('#ornithine-check').removeClass('hidden');
});

$(".ornithine-remove").on("click", function(){
	var product_id = $("#ornithine-select").val();
	
	
	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})
	$(this).hide();

	$("#ornithine-select").attr("disabled", false);
	$("#ornithine-options").collapse('show');
	$(".ornithine-add").show();
	$('#ornithine-check').addClass('hidden');
});

$("#ornithine-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-ornithine-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#ornithine-size").text(size+ "/serving")
	$("#ornithine-price").text(" $" + option + " ($" + price_per_serving + "/serving)");
})


$(".taurine-add").on("click", function(added){

	var variation = $("#taurine-select").val();

	
	
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});

	$(this).hide();

	$("#taurine-select").attr('disabled', true);
	$("#taurine-options").collapse('hide');
	$(".taurine-remove").show();
	$("#taurine-check").removeClass('hidden');

});

$(".taurine-remove").on("click", function(){
	var product_id = $("#taurine-select").val();
	
	
	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})
	$(this).hide();

	$("#taurine-select").attr("disabled", false);
	$("#taurine-options").collapse('show');
	$(".taurine-add").show();
	$('taurine-check').addClass('hidden');
});

$("#taurine-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-taurine-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#taurine-size").text(size+ "/serving")
	$("#taurine-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})

$(".cordyceps-add").on("click", function(added){

	var variation = $("#cordyceps-select").val();

	
	
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});

	$(this).hide();

	$("#cordyceps-select").attr('disabled', true);
	$("#cordyceps-options").collapse('hide');
	$(".cordyceps-remove").show();
	$("#cordyceps-check").removeClass('hidden');
});

$(".cordyceps-remove").on("click", function(){
	var product_id = $("#cordyceps-select").val();
	
	
	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})
	$(this).hide();

	$("#cordyceps-select").attr("disabled", false);
	$("#cordyceps-options").collapse('show');
	$(".cordyceps-add").show();
	$('#cordyceps-check').addClass('hidden');
});

$("#cordyceps-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-cordyceps-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#cordyceps-size").text(size+ "/serving")
	$("#cordyceps-price").text(" $" + option + " ($" + price_per_serving + "/serving)")
})

$(".rhodiola_rosea-add").on("click", function(added){

	var variation = $("#rhodiola_rosea-select").val();

	
	
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});

	$(this).hide();

	$("#rhodiola_rosea-select").attr('disabled', true);
	$("#rhodiola_rosea-options").collapse('hide');
	$(".rhodiola_rosea-remove").show();
	$('#rhodiola-rosea-check').removeClass('hidden');

});

$(".rhodiola_rosea-remove").on("click", function(){
	var product_id = $("#rhodiola_rosea-select").val();
	
	
	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})
	$(this).hide();

	$("#rhodiola_rosea-select").attr("disabled", false);
	$("#rhodiola_rosea-options").collapse('show');
	$(".rhodiola_rosea-add").show();
	$('#rhodiola-rosea-check').addClass('hidden');
});

$("#rhodiola_rosea-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-rhodiola_rosea-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#rhodiola_rosea-size").text(size+ "/serving")
	$("#rhodiola_rosea-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})

$(".hmb-add").on("click", function(added){

	var variation = $("#hmb-select").val();
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});

	$(this).hide();

	$("#hmb-select").attr('disabled', true);
	$("#hmb-options").collapse('hide');
	$(".hmb-remove").show();
	$('#hmb-check').removeClass('hidden');

});

$(".hmb-remove").on("click", function(){
	var product_id = $("#hmb-select").val();
	
	
	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})
	$(this).hide();

	$("#hmb-select").attr("disabled", false);
	$("#hmb-options").collapse('show');
	$(".hmb-add").show();
	$('hmb-check').addClass('hidden');
});

$("#hmb-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-hmb-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#hmb-size").text(size+ "/serving")
	$("#hmb-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})

$(".ashwagandha-add").on("click", function(added){

	var variation = $("#ashwagandha-select").val();

	
	
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});

	$(this).hide();

	$("#ashwagandha-select").attr('disabled', true);
	$("#ashwagandha-options").collapse('hide');
	$(".ashwagandha-remove").show();
	$("#ashwagandha-check").removeClass('hidden');
});

$(".ashwagandha-remove").on("click", function(){
	var product_id = $("#ashwagandha-select").val();
	
	
	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})
	$(this).hide();

	$("#ashwagandha-select").attr("disabled", false);
	$("#ashwagandha-options").collapse('show');
	$(".ashwagandha-add").show();
	$("#ashwagandha-check").addClass('hidden')
});

$("#ashwagandha-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-ashwagandha-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#ashwagandha-size").text(size+ "/serving")
	$("#ashwagandha-price").text(" $" + option + " ($" + price_per_serving + "/serving)")
})

$(".l_tyrosine-add").on("click", function(added){

	var variation = $("#l_tyrosine-select").val();

	
	
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});

	$(this).hide();

	$("#l_tyrosine-select").attr('disabled', true);
	$("#l_tyrosine-options").collapse('hide');
	$(".l_tyrosine-remove").show();
	$("#l-tyrosine-check").removeClass('hidden');
});

$(".l_tyrosine-remove").on("click", function(){
	var product_id = $("#l_tyrosine-select").val();
	
	
	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})
	$(this).hide();

	$("#l_tyrosine-select").attr("disabled", false);
	$("#l_tyrosine-options").collapse('show');
	$(".l_tyrosine-add").show();
	$('#l-tyrosine-check').addClass('hidden');
});

$("#l_tyrosine-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-l_tyrosine-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#l_tyrosine-size").text(size+ "/serving")
	$("#l_tyrosine-price").text(" $" + option + " ($" + price_per_serving + "/serving)")
})

$(".betaine-add").on("click", function(added){

	var variation = $("#betaine-select").val();

	
	
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});

	$(this).hide();

	$("#betaine-select").attr('disabled', true);
	$("#betaine-options").collapse('hide');
	$(".betaine-remove").show();
	$('#betaine-check').removeClass('hidden')
});

$(".betaine-remove").on("click", function(){
	var product_id = $("#betaine-select").val();
	
	
	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})
	$(this).hide();

	$("#betaine-select").attr("disabled", false);
	$("#betaine-options").collapse('show');
	$(".betaine-add").show();
	$('#betaine-check').addClass('hidden')
});

$("#betaine-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-betaine-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-serving-size');
	$("#betaine-size").text(size+ "/serving")
	$("#betaine-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

})

$(".flavor-add").on("click", function(added){

	var variation = $("#flavor-select").val();

	
	
	$.ajax({
		url: '/shopping/preworkout/',
		type: 'POST',
		data: {'variation': variation,},
	});

	$(this).hide();

	$("#flavor-select").attr('disabled', true);
	$("#flavor-options").collapse('hide');
	$(".flavor-remove").show();

});

$(".flavor-remove").on("click", function(){
	var product_id = $("#flavor-select").val();
	
	
	$.ajax({
		url : '/shopping/preworkout/remove/' ,
		type : 'POST',
		data : {'product_id': product_id},
	})
	$(this).hide();

	$("#flavor-select").attr("disabled", false);
	$("#flavor-options").collapse('show');
	$(".flavor-add").show();
});

$("#flavor-select").change(function(){
	console.log("change detected");
	var option = Number($('option:selected', this).attr('data-flavor-price')).toFixed(2);
	var price_per_serving = (option / 30).toFixed(2);
	var size = $('option:selected', this).attr('data-title');
	$(".flavor-size").text(size)
	$("#flavor-price").text(" $" + option + " ($" + price_per_serving + "/serving)")

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




