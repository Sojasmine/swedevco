$(document).ready(function(){
$('.sidenav').sidenav({edge: "right"});
$('.collapsible').collapsible();
$('input#input_text, textarea#textarea2').characterCounter();
$('select').formSelect();
$('.datepicker').datepicker({
    format: "dd mmm, yyyy",
    yearRange: 3,
    showClearBtn: true,
    i18n: {
      done: "Select"
    }
  });

});