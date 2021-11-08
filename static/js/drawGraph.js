function drawGraph(data){

	if (data !== "") {
		console.log(data)
		window.addEventListener('load', function () {
		var chart = dc.rowChart("#chart-01");
	    var ndx = crossfilter(data);

	    var dim = ndx.dimension(function(d) {return d["city_name"]; });
	    var group = dim.group().reduceSum(function(d) {return d.size;});

	    chart
	    .width(300)
	      .height(510)
	        .dimension(dim)
	        .group(group)
	        .ordering(function(d) { return -d.value })
	        .colors(['#6baed6'])
	        .elasticX(true)
	        .labelOffsetY(10)
	        .label(d => d.key + ': ' + d.value)
	        .xAxis().ticks(4);

	       dcCharts = [chart];
	       dc.renderAll();



	})
	}
	
}