
			//Width and height
			var w = 960;
			var h = 600;
      var statesTweets;
      // Define map projection
			var projection = d3.geoAlbersUsa()
									.translate([w/2, h/2])
									.scale([1280]);

		 //Define path generator
		 var path = d3.geoPath()
							.projection(projection);
		 var color = d3.scaleQuantize()
						  .range(['#f7fbff','#deebf7','#c6dbef','#9ecae1','#6baed6','#4292c6','#2171b5','#084594']);
						 //http://colorbrewer2.org/#type=sequential&scheme=Blues&n=8

			//Create SVG element
			var svg = d3.select("body")
						.append("svg")
						.attr("width", w)
						.attr("height", h);

			var x = d3.scaleLinear()
					.domain([0, 1])
			    .rangeRound([600, 860]);


			var g = svg.append("g")
			    .attr("class", "key")
			    .attr("transform", "translate(0,40)");

			g.selectAll("rect")
			  .data(color.range().map(function(d) {
			      d = color.invertExtent(d);
			      if (d[0] == null) d[0] = x.domain()[0];
			      if (d[1] == null) d[1] = x.domain()[1];
			      return d;
			    }))
			  .enter().append("rect")
			    .attr("height", 8)
			    .attr("x", function(d) { return x(d[0]); })
			    .attr("width", function(d) { return x(d[1]) - x(d[0]); })
			    .attr("fill", function(d) { return color(d[0]); });

		g.append("text")
		    .attr("class", "caption")
		    .attr("x", x.range()[0])
		    .attr("y", -6)
		    .attr("fill", "#000")
		    .attr("text-anchor", "start")
		    .attr("font-weight", "bold")
		    .text("Population Rate Usage of #NeverAgain");

		g.call(d3.axisBottom(x)
		    .tickSize(13)
		    .tickFormat(function(x, i) { return i ? x : x + "%"; })
		    .tickValues(color.domain()))
		  .select(".domain")
		    .remove();

      d3.json("day4Tweets.json", function(error, data){
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

        color.domain([
          d3.min(newStateJSON, function(d) { return d.value; }),
          d3.max(newStateJSON, function(d) { return d.value; })
        ]);
        //Load in GeoJSON data
				d3.json("us-states.json", function(json) {
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

					//Bind statesTweets and create one path per GeoJSON feature
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


		 				//Define quantize scale to sort data values into buckets of color

				});


			});
