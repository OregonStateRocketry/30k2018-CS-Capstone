var flight, data, flightList= [];

document.body.addEventListener('click',function(event){
  /*Event listener for flight selection button
    Should hide flight select div, reveal the data select div, and save flight selection.
    If multi is selcted, should reveal multi div instead*/
  if (event.target.id=="flightSubmit" && document.getElementById('flightField').value!="multi"
  && document.getElementById('flightField').value!=""){
      /*Show next Selection*/
      document.getElementById('dataSelect').classList.toggle('hide');
      document.getElementById('flightSelect').classList.toggle('hide');
      /*Save flight data and display above data select*/
      flightList.push(document.getElementById('flightField').value);
      var showFlight= document.createElement('h2');
      var flightText1= document.createTextNode('Flight: ');
      var flightText2= document.createTextNode(flightList[0]);
      showFlight.appendChild(flightText1);
      showFlight.appendChild(flightText2);
      var element = document.getElementById("displaySelect");
      element.appendChild(showFlight);
    }

  /*Swap view to multiple flights selection*/
  if (event.target.id=="flightSubmit" && document.getElementById('flightField').value=="multi"
  && document.getElementById('flightField').value!=""){
    /*Show next Selection*/
    document.getElementById('multiSelect').classList.toggle('hide');
    document.getElementById('flightSelect').classList.toggle('hide');
  }

  /*Event listener for multi flight selection button*/
  if (event.target.id=="multiAdd"||event.target.id=="multiSubmit"
  && document.getElementById('multiField').value!=""){
      /*Save flight data and display above data select*/
      flightList.push(document.getElementById('multiField').value);
      if (flight ==undefined){
        var flightTitle= document.createTextNode('Flights Selected: ');
        var element = document.getElementById("displayTitle");
        element.appendChild(flightTitle);
      }
      flight=(document.getElementById('multiField').value);
      var flightVal= document.createTextNode(flight);
      var flightText= document.createElement("li")
      var element = document.getElementById("displayList");
      flightText.appendChild(flightVal);
      element.appendChild(flightText);

      if (event.target.id=="multiSubmit"){
        document.getElementById('dataSelect').classList.toggle('hide');
        document.getElementById('multiSelect').classList.toggle('hide');
      }
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

    /*TODO Call query function/ page change*/
    }
});
