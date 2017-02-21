
$(".Caffeine-add").on("click", function(added){

	var variation = $("#Caffeine-select").val();

	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	});

	console.log("item added");

	$(this).hide();

	$("#Caffeine-select").attr('disabled', true);
	$(".Caffeine-remove").show();

});



$(".Caffeine-remove").on("click", function(){
	var variation = $("#Caffeine-select").val();
	$.ajax({
		url : '/shopping/remove?id=' + variation,
		type: 'GET',
	})

	$("#Caffeine-select").attr("disabled", false);
	$(this).hide();
	$(".Caffeine-add").show();
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
	var variation = $("#theanine-select").val();
	$.ajax({
		url : '/shopping/remove?id=' + variation,
		type: 'GET',
	})

	$("#theanine-select").attr("disabled", false);
	$(this).hide();
	$(".theanine-add").show();
});


$(document).ready(function() {
	var current_caffeine_price = $("#Caffeine-select option:selected").attr("data-caffeine-price");
	var caffeine_price_per_serving = (current_caffeine_price / 30).toFixed(2);
	console.log(caffeine_price_per_serving);
	$("#caffeine-price").text("$ " + current_caffeine_price + " ($" + caffeine_price_per_serving + "/serving)");
	console.log(current_caffeine_price);

});

$("#Caffeine-select").change(function(){
	console.log('change fired')
	var caffeine_selected = Number($("#Caffeine-select").val());
	console.log(typeof(caffeine_selected));
	var current_caffeine_price = caffeine_selected.toFixed(2);	
	var caffeine_price_per_serving = (current_caffeine_price / 30).toFixed(2);
	$("#caffeine-price").text("$ " + current_caffeine_price + " ($" + caffeine_price_per_serving + "/serving)")

})


