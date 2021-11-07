let refreshButton, yearSelection, macroStatSelection; 

let queryString = 
window.addEventListener('load', function () {
  refreshButton= document.getElementById('refresh');
  macroStatSelection = document.getElementById('macrostat-selection');
  yearSelection = document.getElementById('year-selection')

  /*refreshButton.onclick = refresh;*/
  //macroStatSelection.onchange = updateQueryString();
  //yearSelection.onchange = updateQueryString();
})

 




function refresh() {
  console.log("refresh")
  var map = anychart.map();
    //updateQuery();
    //draw();
}

function drawMapWithData(data) {
  if (data !== "") {
  anychart.onDocumentReady(function () {
    var map = anychart.map();

    map.geoData(anychart.maps['united_states_of_america']);

    var series = map.bubble(data);
    console.log(data)
    series.labels().format("{%city_name}");
    series.tooltip().format("{%size}");
    series.tooltip().titleFormat("{%city_name}");

    map.maxBubbleSize(45);
    map.minBubbleSize(15);

    map.container('map');
    map.draw();
   })
  } else {
    anychart.onDocumentReady(function () {

  var map = anychart.map();

    var data = [
      {'id': 'US.MA', 'value': 300},
      {'id': 'US.MN', 'value': 230}, 
      {'id': 'US.MT', 'value': 240}, 
      {'id': 'US.ND', 'value': 275}, 
      {'id': 'US.HI', 'value': 130}, 
      {'id': 'US.ID', 'value': 190}, 
      {'id': 'US.WA', 'value': 100},         
      {'id': 'US.AZ', 'value': 305},                
      {'id': 'US.CA', 'value': 190}, 
      {'id': 'US.CO', 'value': 300},
      {'id': 'US.NV', 'value': 230}, 
      {'id': 'US.NM', 'value': 240}, 
      {'id': 'US.OR', 'value': 275}, 
      {'id': 'US.UT', 'value': 130}, 
      {'id': 'US.WY', 'value': 190}, 
      {'id': 'US.AR', 'value': 100},         
      {'id': 'US.IA', 'value': 305},                
      {'id': 'US.KS', 'value': 190}, 
      {'id': 'US.MO', 'value': 300},
      {'id': 'US.NE', 'value': 230}, 
      {'id': 'US.OK', 'value': 240}, 
      {'id': 'US.SD', 'value': 275}, 
      {'id': 'US.LA', 'value': 130}, 
      {'id': 'US.TX', 'value': 190}, 
      {'id': 'US.CT', 'value': 100},         
      {'id': 'US.NH', 'value': 305},                
      {'id': 'US.RI', 'value': 190}, 
      {'id': 'US.VT', 'value': 300},
      {'id': 'US.AL', 'value': 230}, 
      {'id': 'US.FL', 'value': 240}, 
      {'id': 'US.GA', 'value': 275}, 
      {'id': 'US.MS', 'value': 130}, 
      {'id': 'US.SC', 'value': 190}, 
      {'id': 'US.IL', 'value': 100},
      {'id': 'US.IN', 'value': 305},  
      {'id': 'US.KY', 'value': 100},  
      {'id': 'US.NC', 'value': 275},     
      {'id': 'US.OH', 'value': 305},                
      {'id': 'US.TN', 'value': 190}, 
      {'id': 'US.VA', 'value': 100},         
      {'id': 'US.WI', 'value': 305},                
      {'id': 'US.WV', 'value': 190}, 
      {'id': 'US.DE', 'value': 300},
      {'id': 'US.MD', 'value': 230}, 
      {'id': 'US.NJ', 'value': 240}, 
      {'id': 'US.NY', 'value': 275}, 
      {'id': 'US.PA', 'value': 130}, 
      {'id': 'US.ME', 'value': 190}, 
      {'id': 'US.MI', 'value': 100},         
      {'id': 'US.AK', 'value': 305},                
      {'id': 'US.DC', 'value': 190}
    ];

    //
    

    // set the series
    var series = map.choropleth(data);
    series.colorScale(anychart.scales.linearColor('#deebf7', '#3182bd'));
    series.hovered().fill('#addd8e');


  
    map.geoData(anychart.maps['united_states_of_america']);
    map.unboundRegions().fill('#eee');


    // set the container
    map.container('map');
    map.draw();
  });
  }
}

