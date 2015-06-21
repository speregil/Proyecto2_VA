var width = 960,
    height = 500;

var projection = d3.geo.mercator()
    .center([0, 20 ])
    .scale(150)
    .rotate([0,0]);

var svg = d3.select("body #mapa").append("svg")
    .attr("width", width)
    .attr("height", height);

var path = d3.geo.path()
    .projection(projection);

var g = svg.append("g");
var g2 = svg.append("g").attr("class","puntoDestino");
var g3 = svg.append("g").attr("class","puntoAccidente");

// load and display the World
d3.json("world-110m2.json", function(error, topology) {

// load and display the cities
d3.json("ciudades.json", function(error, data) {
    g.selectAll("circle")
       .data(data)
       .enter()
       .append("circle")
       .attr("cx", function(d) {
               return projection([d.lon, d.lat])[0];
       })
       .attr("cy", function(d) {
               return projection([d.lon, d.lat])[1];
       })
       .attr("r", 5)
       .style("fill", "#F20057")
     .on("mouseover", function(d) {

          //Get this bar's x/y values, then augment for the tooltip
          var xPosition = parseFloat(d3.select(this).attr("cx"));
          var yPosition = parseFloat(d3.select(this).attr("cy"));

          //Update the tooltip position and value
          d3.select("#tooltip")
            .style("left", xPosition + "px")
            .style("top", yPosition + "px")           
            .select("#value")
            .text(d.city + ", " + d.country + "\n" + "destino: " + d.cityDestino + "\n" + "accidente: " + d.cityAccidente + "   "+ xPosition + " - " + yPosition);
            
                        
            g2.selectAll("circle")
                  .data(data)
                  .enter()
                  .append("circle")
              .attr("cx", function(d) {

                if (xPosition == projection([d.lonDestino, d.latDestino])[0]) {
                  return projection([d.lonDestino, d.latDestino])[0];
                };
                
              })
              .attr("cy", function(d) {
                if (yPosition == projection([d.lonDestino, d.latDestino])[1]) {
                  return projection([d.lonDestino, d.latDestino])[1];
                };
                   
               })
               .attr("r", 5);
            g3.selectAll("circle")
                  .data(data)
                  .enter()
                  .append("circle")
              .attr("cx", function(d) {
                if (false) {
                  return projection([d.lonAccidente, d.latAccidente])[0];
                };
                
              })
              .attr("cy", function(d) {
                if (false) {
                  return projection([d.lonAccidente, d.latAccidente])[1];
                };
                   
               })
               .attr("r", 5);
              
          //Show the tooltip
          d3.select("#tooltip").classed("hidden", false);

         })
         .on("mouseout", function() {
           
           g2.selectAll("circle").remove();
         g3.selectAll("circle").remove();
          //Hide the tooltip
          d3.select("#tooltip").classed("hidden", true);
          
         });
     
     g.selectAll("text")
       .data(data)
       .enter()
     .append("text") // append text
       .attr("x", function(d) {
               return projection([d.lon, d.lat])[0];
       })
       .attr("y", function(d) {
               return projection([d.lon, d.lat])[1];
       })
       .attr("dy", -7) // set y position of bottom of text
      .style("fill", "black") // fill the text with the colour black
      .attr("text-anchor", "middle") // set anchor y justification
      .text(function(d) {return d.city;}); // define the text to display
});


g.selectAll("path")
      .data(topojson.feature(topology, topology.objects.countries)
.features)
    .enter()
      .append("path")
      .attr("d", path)
});

// zoom and pan
var zoom = d3.behavior.zoom()
    .on("zoom",function() {
        g.attr("transform","translate("+ 
            d3.event.translate.join(",")+")scale("+d3.event.scale+")");
        g.selectAll("circle")
            .attr("d", path.projection(projection));
        g.selectAll("path")  
            .attr("d", path.projection(projection)); 
    
    g2.attr("transform","translate("+ 
            d3.event.translate.join(",")+")scale("+d3.event.scale+")");
        g2.selectAll("circle")
            .attr("d", path.projection(projection));
        g2.selectAll("path")  
            .attr("d", path.projection(projection)); 
      
    g3.attr("transform","translate("+ 
            d3.event.translate.join(",")+")scale("+d3.event.scale+")");
        g3.selectAll("circle")
            .attr("d", path.projection(projection));
        g3.selectAll("path")  
            .attr("d", path.projection(projection)); 
    

  });

svg.call(zoom)