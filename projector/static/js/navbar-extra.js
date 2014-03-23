$(function() {
  // Fix input element click problem
  $('.dropdown-menu').click(function(e) {
    e.stopPropagation();
  });
  
  $("#proteinControls").detach().appendTo($("#insertProteinControlsHere"));
});