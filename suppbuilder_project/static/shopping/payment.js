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


$("input:radio").change(function() {

  var shipping_method_id = $(this).attr("id");
  var order_id = $("#order-id").val();


  $.ajax({
    url: '/shopping/stripe-update-order/',
    type: 'POST',
    dataType: "json",
    data: {'shipping_method_id': shipping_method_id, 'order_id' : order_id,},
    success : function(data){
      console.log(data.shipping_price[0]/100);
      var shipping_price = data.shipping_price[0]/100;
      var order_total = (data.order.amount/100).toFixed(2);
      $("#cart-total").text(order_total);
      $("#shipping-price").text(shipping_price);
    }, 
    error : function(data){
      console.log("There was an error captain")
    }
  });


});

$("#discount").click(function(){

	var name = $("#discount-code").val();
  var order_id = $("#order-id").val();

  $.ajax({
    url : '/shopping/discount/',
    type : 'POST',
    dataType: "json",
    data : {'name' : name, 'order_id' : order_id},
    success : function(data){
      console.log(data)
      if (data == 'Invalid code'){
        $("input[type=text]#discount-code").val(data);
      }
      else {
        console.log(typeof(data));
        var discount_amount = (data.discount_amount/100).toFixed(2);
        var order_total = (data.order.amount/100).toFixed(2);
        $("#discount-section").html("<p> Huzzah! discount applied! </p>");
        $("#discount-title").text("Discount:");
        $("#discount-amount").text("$ " + discount_amount);
        $("#cart-total").text(order_total)
      }
    },
    error: function(data){
      console.log("There was an error captain")
    }
  })

});
