$(document).ready(function() {

  /*
  make the how it works section slide up when the 
  user scrolls down to that section.
  offset by 70%, the default would have the entire
  page blank before the section slides up
  */
  $(".js--wp-1").waypoint(function(direction){
    $(".js--wp-1").addClass('animated slideInUp');
  }, {
    offset: "70%"
  });


    $(".js--wp-2").waypoint(function(direction){
    $(".js--wp-2").addClass('animated fadeIn');
  }, {
    offset: "70%"
  });
});