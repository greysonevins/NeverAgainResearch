var w = 960;
var h = 600;
var statesTweets;

var projection = d3.geoAlbersUsa()
						.translate([w/2, h/2])
						.scale([1280]);
// Change variable here to call other days
var day = "4"

var path = d3.geoPath()
				.projection(projection);
var color = d3.scaleQuantize()
				.domain([0,114])
			  .range(['#f7fbff','#deebf7','#c6dbef','#9ecae1','#6baed6','#4292c6','#2171b5','#084594']);
			 //http://colorbrewer2.org/#type=sequential&scheme=Blues&n=8

var svg = d3.select("body")
			.append("svg")
			.attr("width", w)
			.attr("height", h);

var x = d3.scaleLinear()
		.domain([0,114])
    .rangeRound([600, 860])


var g = svg.append("g")
    .attr("class", "key")
    .attr("transform", "translate(0,40)");

g.selectAll("rect")
  .data(color.range().map(function(d) {
      d = color.invertExtent(d);
      if (d[0] == null) d[0] = x.domain()[0];
      if (d[1] == null) d[1] = x.domain()[1];
			var newD = [Math.ceil(d[0]), Math.ceil(d[1])]
      return newD;
    }))
  .enter().append("rect")
    .attr("height", 8)
    .attr("x", function(newD) { return x(newD[0]); })
    .attr("width", function(newD) { return x(newD[1]) - x(newD[0]); })
    .attr("fill", function(newD) { return color(newD[0]); });

g.append("text")
  .attr("class", "caption")
  .attr("x", x.range()[0])
  .attr("y", -6)
  .attr("fill", "#000")
  .attr("text-anchor", "start")
  .attr("font-weight", "bold")
	.text(`Population Rate per million Usage of #NeverAgain Day ${day}`);

g.call(d3.axisBottom(x)
  .tickSize(13)
  .tickFormat(function(x) { return x   })
  .tickValues(color.range().map( function(d) { return color.invertExtent(d)[1] })))
		.select(".domain")
  .remove();

d3.json(`data/day${day}Tweets.json`, function(error, data){
	var minMax;

	d3.json("data/minMax.json", function(json){
		color.domain([json.minValue, json.maxValue]);
		x.domain([
			json.minValue,
			json.maxValue
		])

	})
  statesTweets = data
  var newStateJSON = [];
  for (var item in statesTweets){
    var stJSON = {
      name : item,
      value: statesTweets[item]
    }
    newStateJSON.push(stJSON)
  }
  var statesTweets = newStateJSON;
  extent = d3.extent(newStateJSON, function (d) {
    return d.value
  })


  //Load in GeoJSON data
	d3.json("/data/us-states.json", function(json) {
		//Merge the ag. data and GeoJSON
		//Loop through once for each ag. data value

		for (var i = 0; i < statesTweets.length; i++) {

			//Grab state name
			var dataState = statesTweets[i].name;

			//Grab statesTweets value, and convert from string to float
			var dataValue = statesTweets[i].value;

			//Find the corresponding state inside the GeoJSON
			for (var j = 0; j < json.features.length; j++) {

				var jsonState = json.features[j].properties.name;

				if (dataState == jsonState) {

					//Copy the statesTweets value into the JSON
					json.features[j].properties.value = dataValue;

					//Stop looking through the JSON
					break;

				}
			}
		}

		svg.selectAll("path")
		   .data(json.features)
		   .enter()
		   .append("path")
		   .attr("d", path)
		   .style("fill", function(d) {
		   		//Get statesTweets value
		   		var value = d.properties.value;

		   		if (value) {
		   			//If value exists…
			   		return color(value);
		   		} else {
		   			//If value is undefined…
			   		return "#ccc";
		   		}
		   });

	});


});
