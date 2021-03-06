var flight, data, flightList= [];

document.body.addEventListener('click',function(event){
  /*Event listener for flight selection button
    Should hide flight select div, reveal the data select div, and save flight selection.*/
  if (event.target.id=="flightSubmit" 
  && document.getElementById('flightField').value!=""){
      /*Show next Selection*/
      document.getElementById('dataSelect').classList.toggle('hide');
      document.getElementById('flightSelect').classList.toggle('hide');
      /*Save flight data and display above data select*/
      flight=document.getElementById('flightField').value;
      var showFlight= document.createElement('h2');
      var flightText1= document.createTextNode('Flight: ');
      var flightText2= document.createTextNode(flight);
      showFlight.appendChild(flightText1);
      showFlight.appendChild(flightText2);
      var element = document.getElementById("displaySelect");
      element.appendChild(showFlight);
    }

  /*Event listener for data selection button
  Should hide data div and save data selection.
  A function should be called to handle the query and page swap*/
  if (event.target.id=="dataSubmit"
  && document.getElementById('dataField').value!=""){
    /*Show next Selection*/
    document.getElementById('dataSelect').classList.toggle('hide');
    document.getElementById('Welcome').classList.toggle('hide');

    /*Save data selection*/
    data=(document.getElementById('dataField').value);

    /*Save flight data and display above data select*/
    var showData= document.createElement('h2');
    var DataText1= document.createTextNode('Data Set: ');
    var DataText2= document.createTextNode(data);
    showData.appendChild(DataText1);
    showData.appendChild(DataText2);
    var element = document.getElementById("displaySelect");
    element.appendChild(showData);

    /* Call query function/ page change*/
	var query = "graph?get="+data+"&fid="+flight+"&";
	window.location.href = "/"+query;
    }
});

/* Add Dynamic Flight ID Selection: Dropdowns should pull from the database  */
function UpdateDropdown() {
    $.getJSON("/q?get=fid", function(data){
        $.each(data,function(key, value){
            /*For each flight ID, create two option elements and append them to both the
            flight selection dropdown menus.
            This has been done twice because two elements must be created in order to append them to each of the dropdowns. */

            //Add option to flight dropdown
            var option = document.createElement('option');
            option.value = value["flight_id"];
            option.text = value["flight_id"];
            var element = document.getElementById("flightField");
                element.appendChild(option);


        });
    });
};
