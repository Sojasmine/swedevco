$(document).ready(function(){
  /* mobile sidenav bar*/
    $('.sidenav').sidenav({edge: "right"});
     /* for the all jobs page*/
    $('.collapsible').collapsible();
  /* for the post_jobs page*/
  $('.datepicker').datepicker({
    format: "dd mmm, yyyy",
    yearRange: 3,
    showClearBtn: true,
    i18n: {
      done: "Select"
    }
  });
$('input#input_text, textarea#textarea2').characterCounter();
    
  });