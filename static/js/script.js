/*
    script.js JavaScript file

    Author: Jerome Israel
    11.08.11, updated 11.11.14
*/


/**
 * ready function to run on page load
 */
$( document ).ready(function() {
	
    $(".results").hide();
    $(".errorMessage").hide();
    $(".CSSTableGenerator").hide();
    $('#latitude_text_box').attr("disabled", "disabled");
    $('#longitude_text_box').attr("disabled", "disabled");
});

$("input[name='group1']").change(function () {
    if ($("#locationRadioButton").is(':checked')) {

        $('#address_text_box').attr("disabled", "disabled"); //.attr("placeholder",'Latitude , Longitude');
        $('.results').css("display","none");
        $('#latitude_text_box').removeAttr("disabled");
        $('#longitude_text_box').removeAttr("disabled");
    }
    else {

        $('#latitude_text_box').attr("disabled", "disabled");
        $('#longitude_text_box').attr("disabled", "disabled");
        $('#address_text_box').removeAttr("disabled"); 
    }
});

/**
 * loadAddressToTextBox loads the Address to text box from the list when selected
 */
function loadAddressToTextBox(text){

    $(".results").hide();
    jQuery('#address_text_box').val(text.name);

}

/**
 *  On input to address Text box event
 */
jQuery('#address_text_box').on('input', function(){

    if ($("#addressRadioButton").is(':checked')) {
        console.log('complete the address');
       // Make a get call to fetch the address for completion
        $.ajax({
         //Local host URL
          //url: "http://localhost:5000/fetchAddress",
          url: "https://lit-spire-7420.herokuapp.com/fetchAddress",
          data: "preaddress=" + $( "#address_text_box" ).val(),
          success: function(data) {

                addresses = jQuery.parseJSON(data);
                console.log(addresses);
                $( ".results" ).empty();
                $(".results").show();
                for (var address in addresses) {

                    $(".results").append("<li ><a href=\"#\" onClick=\"loadAddressToTextBox(this);\" name=\"" + address + "\" >" 
                    	+ address + "</a></li>");
                }
            }
          
        });

        $("#address_text_box").focus(function(){
          $('.results').css("display","block");
        });
    }
    
});

/**
 *  submit method submits the input and makes an Ajax call to the 
 *  backend to fetch the closest locations
 */
function submit(){

    $(".CSSTableGenerator").hide();

    //Delete Existing Result rows
    deleteRows();

    if($("#locationRadioButton").is(':checked')) {
        
        //validate location
		if($('#latitude_text_box').val().length > 0 && $('#longitude_text_box').val().length > 0){

            lat = $('#latitude_text_box').val()
            lon = $('#longitude_text_box').val()

            var validlat = !isNaN(lat);
            var validlon = !isNaN(lon);

            if(validlat && validlon){

                queryLocation(lat, lon);

            } else{

                alert('You have entered an invalid location data. Please enter only floating numbers for Latitude and Longitude!');
            }
        } else {

            alert('Latitude and longitude cannot be empty when location is selected');
        }
        
    } else {
        //Check for address
        if($("#address_text_box").val().length > 0){

            queryAddress();
        } else {

            alert('Address field cannot be empty');
        }

    }
    
    
}

/**
 *  queryLocation method makes a call to the fetchNeighborsFromAddress webservice
 */
function queryLocation(lat, lon){

    console.log('queryLocation');

    $.ajax({
         //Local host URL
          //url: "http://localhost:5000/fetchNeighborsFromLocation",
          url: "https://lit-spire-7420.herokuapp.com/fetchNeighborsFromLocation",
          data: "latitude=" + lat + "&longitude=" + lon,
          success: function(data) {

                result = JSON.parse(data);

                if(result['success']){
                    
                    loadResults(result['result']);
                } else{
                    $(".results").hide();
                    $(".errorMessage").fadeIn();
                }
            }
          
        });
}

/**
 *  queryAddress method makes a call to the fetchNeighborsFromAddress webservice
 */
function queryAddress(){

    $.ajax({
         //Local host URL
          //url: "http://localhost:5000/fetchNeighborsFromAddress",
          //Heroku URL
          url: "https://lit-spire-7420.herokuapp.com/fetchNeighborsFromAddress",
          data: "address=" + $( "#address_text_box" ).val(),
          success: function(data) {

                result = JSON.parse(data);

                if(result['success']){
                    
                    loadResults(result['result']);
                } else{
                    $(".results").hide();
                    $(".errorMessage").fadeIn();
                }
            }
          
        });
}

/**
 *  loadResults method loads the response (if success) to the table
 */
function loadResults(result){

    for (var k in result) {

        data = result[k];
        //Result is success. Show results on screen
        // Find a <table> element with id="resultsTable":
        var table = document.getElementById("resultsTable");
        var rowCount = table.rows.length;
        // Create an empty <tr> element and add it to the 1st position of the table:
        var row = table.insertRow(rowCount);

        // Insert new cells (<td> elements) at the appropriate position of the "new" <tr> element:
        var locationId  = row.insertCell(0);
        var name        = row.insertCell(1);
        var type        = row.insertCell(2);
        var foodItems   = row.insertCell(3);
        var address     = row.insertCell(4);
        var latitude    = row.insertCell(5);
        var longitude   = row.insertCell(6);
        var status      = row.insertCell(7);
        var distance    = row.insertCell(8);

        // Add text to the new cells:
        locationId.innerHTML    = k;
        name.innerHTML          = data['name'];
        type.innerHTML          = data['type'];
        foodItems.innerHTML     = data['food'];
        address.innerHTML       = data['address'];
        latitude.innerHTML      = data['latitude'];
        longitude.innerHTML     = data['longitude'];
        status.innerHTML        = data['status'];
        distance.innerHTML      = data['distance'];

    }
    $(".CSSTableGenerator").fadeIn();

}

/*
 *	deleteRows method delets table rows
 */
function deleteRows(){

    var tbl = document.getElementById("resultsTable");
    var tblRows = document.getElementById("resultsTable").getElementsByTagName("tr").length;

    if(tblRows > 1){

        tbl.deleteRow(1);
        deleteRows();
    }
}
