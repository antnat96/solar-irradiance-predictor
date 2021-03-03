$(document).ready(function() {

  $(".flight-row").on("click", function() {
    $("#flight-modal-" + $(this).prop("id").split("-")[2]).modal("show");
  })

  $(".flight-row").hover(function() {
    $(this).closest("tr").addClass("flight-row-animation");
  }, function() {
    $(this).closest("tr").removeClass("flight-row-animation");
  })

  // Sort table base on the col clicked
  function sortTable(numberCol){
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("arrivals_table");
    switching = true;
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
      //start by saying: no switching is done:
      switching = false;
      rows = table.rows;
      /*Loop through all table rows (except the
      first, which contains table headers):*/
      for (i = 1; i < (rows.length - 1); i++) {
        //start by saying there should be no switching:
        shouldSwitch = false;
        /*Get the two elements you want to compare,
        one from current row and one from the next:*/
        x = rows[i].getElementsByTagName("TD")[numberCol];
        y = rows[i + 1].getElementsByTagName("TD")[numberCol];
        //check if the two rows should switch place:
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
            //if so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
        }
      }
      if (shouldSwitch) {
        /*If a switch has been marked, make the switch
        and mark that a switch has been done:*/
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
      }
    }
  }

  $("#col-id").on("click",function(){
    // console.log("Sorting by col-id");
    sortTable(0)
  });
  
  $("#col-arr-date").on("click",function(){
    // console.log("Sorting by col-arr-date");
    sortTable(1)
  });
  
  $("#col-arr-location").on("click",function(){
    // console.log("Sorting by col-arr-location");
    sortTable(2)
  });
  
  $("#col-land-time").on("click",function(){
    // console.log("Sorting by col-land-time");
    sortTable(3)
  });
  
  $("#col-flt-time").on("click",function(){
    // console.log("Sorting by col-flt-time");
    sortTable(4)
  });
  
  $("#col-cargo-wt").on("click",function(){
    // console.log("Sorting by col-cargo-wt");
    sortTable(5)
  });
  
  $("#col-cargo-descri").on("click",function(){
    // console.log("Sorting by col-cargo-descri");
    sortTable(6)
  });
  
  $("#col-cargo-pieces").on("click",function(){
    // console.log("Sorting by col-cargo-pieces");
    sortTable(7)
  });
});