let refreshButton, yearSelection, macroStatSelection; 

let queryString = 
window.addEventListener('load', function () {
  refreshButton= document.getElementById('refresh');
  macroStatSelection = document.getElementById('macrostat-selection');
  yearSelection = document.getElementById('year-selection')

})

 




function refresh() {
  console.log("refresh")
  var map = anychart.map();
}

function drawMapWithData(data) {
  anychart.onDocumentReady(function () {
    var map = anychart.map();

    map.geoData(anychart.maps['united_states_of_america']);

    var series = map.bubble(data);
    console.log('data1' in data[0])
    series.labels().format("{%city_name}");
    if ('data1' in data[0]){
      series.tooltip().format("Data1: {%data1}, Data2: {%data2}");
    }
    else {
      series.tooltip().format("{%size}");
    }
    series.tooltip().titleFormat("{%city_name}");

    map.maxBubbleSize(45);
    map.minBubbleSize(15);

    map.container('app-maparea');
    map.draw();


    



    


   })
  }

