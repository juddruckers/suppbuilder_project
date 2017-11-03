$(document).ready(function() {

  // icon animation on scroll

  $(".js--wp-1").waypoint(function(direction){
    $(".js--wp-1").addClass('animated slideInUp');
  }, {
    offset: "70%"
  });

});