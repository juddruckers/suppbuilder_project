

$("#Caffeine-button").on("click", function(){
	var variation = $("#Caffeine-select").val();
	$.ajax({
		url: '/shopping/add?id=' + variation,
		type: 'GET',
	})
});

$("#Caffeine-remove").on("click", function(){
	var variation = $("#Caffeine-select").val();
	$.ajax({
		url : '/shopping/remove?id=' + variation,
		type: 'GET',
	})
});


