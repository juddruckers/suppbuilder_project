

$('.payment-delete').click(function(){
	var pk = $(this).data("token");
	var image = $(this).data('image');
	var lastfour = $(this).data('lastfour');
	var method = $(this).data('method');
	var expiration = $(this).data('expire');


  $('#payment-token').attr('value', pk);


	$("div.modal-body").html(
		"<p><img src="+ image +" height='21' width='34'> " + method +  " ****" + lastfour + " </p> "
	);




});

