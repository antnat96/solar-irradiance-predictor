$(document).ready(function() {
  $(".flight-row").on("click", function() {
    $("#flight-modal-" + $(this).prop("id").split("-")[2]).modal("show");
  })

  $(".flight-row").hover(function() {
    $(this).closest("tr").addClass("flight-row-animation");
  }, function() {
    $(this).closest("tr").removeClass("flight-row-animation");
  })

  $(".editable-div").hover(function() {
    // Get current data
    startData = $(this).text().trim();
    // Set the innerHTML to an empty string for now
    $(this).text("");
    // Create new input element
    let newInput = document.createElement("input");
    // Give it its type and class
    newInput.setAttribute("type", "textarea");
    newInput.setAttribute("id", "current-edit");
    // Set its text content
    newInput.setAttribute("value", startData);
    // Add it
    $(this).append(newInput);

  }, 
  // On hover out
  function() {
    // Capture the input
    let newData = $("#current-edit").val().trim(); 
    // If new input is different, mark the div with a changed class
    if (newData !== startData) {
      saveData($(this).attr("id").split("-")[0], $(this).attr("id").split("-")[1], newData);
    }        
    // Remove the input field 
    $("#current-edit").remove();
    // Set the text to the changed text
    $(this).text(newData);
  })

  function saveData(field, flightId, newData) {

    $.getJSON($SCRIPT_ROOT + '/editFlight', {
      id: flightId,
      field: field,
      newData: newData
    }, 
    function(data) {
      if (data.updated === "1") {
        $("#" + field + "-" + flightId).addClass("changed");
      }
      else {
        $("#" + field + "-" + flightId).addClass("failed");
      }
    });
    
    $("#flight-modal-" + flightId).on("hidden.bs.modal", function() {
      location.reload();
    })

  }
  $(".del-flt-btn").on("click", function() {
    $(".flight-row").off("click"); // Prevents event listener on table row from firing
    let flight_id_to_delete = $(this).attr("id").split("-")[1];
    if (confirm("Are you sure you want to delete this record? If so, select OK")) {
      $.getJSON($SCRIPT_ROOT + '/deleteFlight', {
        id: flight_id_to_delete
      }, 
      function(data) {
        //console.log(data);
      });
    }
    location.reload();
  });

  // Sort table base on the col clicked
  function sortTable(numberCol){
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("flights_table");
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

  $("#col-dep-date").on("click",function(){
    // console.log("Sorting by col-dep-date");
    sortTable(1)
  });
  
  $("#col-dep-location").on("click",function(){
    // console.log("Sorting by col-dep-location");
    sortTable(2)
  });

  $("#col-arr-date").on("click",function(){
    // console.log("Sorting by col-arr-date");
    sortTable(3)
  });

  $("#col-arr-location").on("click",function(){
    // console.log("Sorting by col-arr-location");
    sortTable(4)
  });

  $("#col-flt-time").on("click",function(){
    // console.log("Sorting by col-flt-time");
    sortTable(5)
  });

  $("#col-cargo-wt").on("click",function(){
    // console.log("Sorting by col-cargo-wt");
    sortTable(6)
  });

  $("#col-acft-type").on("click",function(){
    // console.log("Sorting by col-acft-type");
    sortTable(7)
  });

  $("#col-tail-num").on("click",function(){
    // console.log("Sorting by col-tail-num");
    sortTable(8)
  });
});