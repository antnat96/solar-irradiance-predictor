$(document).ready(function() {
        
    // Handler for the "Add Flight" button
    $("#add-flight-button").on("click", function() {

      if (inputIsValid()) {
        var jqxhr = $.getJSON($SCRIPT_ROOT + '/addFlightLogic', {
          id: Math.random().toString(36).slice(2).substr(0, 5).toUpperCase(),        
          aircraft_type : $("#aircraftType").val(),
          aircraft_tail_num: $("#tailNumber").val(),
          departure_date : $("#departureDate").val(),
          departure_location : $("#departureLocation").val(),
          departure_airport_code : $("#departureAirportCode").val(),
          departure_time_local: $("#departureTimeLocal").val(),
          departure_time_zulu: $("#departureTimeZulu").val(),
          arrival_date: $("#arrivalDate").val(),
          arrival_location: $("#arrivalLocation").val(),
          arrival_airport_code: $("#arrivalAirportCode").val(),
          arrival_time_local: $("#arrivalTimeLocal").val(),
          arrival_time_zulu: $("#arrivalTimeZulu").val(),
          flight_time : $("#flightTime").val(),
          cargo_num_of_items: $("#itemsNumber").val(),
          cargo_weight_lbs: $("#weightPounds").val(),
          cargo_weight_kg: $("#weightKilograms").val(),
          cargo_loading_agents: $("#loadingAgents").val(),
          cargo_description: $("#cargoDescription").val()
        })
        .done(function(data) {
          if (data.flight_added === "1") {
            $("#success_modal").modal("show");
            $("#success_modal").on("hidden.bs.modal", function() {
              $(":input", "#aircraft-info").val("");
              $(":input", "#flight-info").val("");
              $(":input", "#cargo-info").val("");
            })
          }
          else {
            window.alert("Oops! Something went wrong.");
          }
        })
        .fail(function( jqxhr, textStatus, error ) {
          var err = textStatus + ", " + error;
          console.log( "Request Failed: " + err );
        });
      }
      else {
        window.alert("Please review your input and make corrections.");
      }
    })

    function inputIsValid() {
      // Getting input elements & values
      var aircraftInfoRaw = document.querySelectorAll("#aircraft-info input");
      var flightInfoRaw = document.querySelectorAll("#flight-info input");
      var cargoInfoRaw = document.querySelectorAll("#cargo-info input");

      // Validating input
      for (var i = 0, element; element = aircraftInfoRaw[i++];) {
          if (element.value == null || element.value == undefined || element.value == "") {
            return false;
          }
      }
      for (var i = 0, element; element = flightInfoRaw[i++];) {
        if (element.value == null || element.value == undefined || element.value == "") {
          return false;
        }
      }
      for (var i = 0, element; element = cargoInfoRaw[i++];) {
        if (element.value == null || element.value == undefined || element.value == "") {
          return false;
        }
      }
      return true;
    }

  });