/**
 *
 */
	
	var dataset;
	var switchFirstTime = true;
	var specificHeightDomainWhenUpdate;
	firstLoad();
	
	function firstLoad() { 		
        console.log("reading guest");        
		var url="trimestre?"+
            "trimestre="+"3";
        d3.json(url, function (e, d) {
            crearArray(d.array);
			console.log(d.array);
        });
	
    }
    
	
	function crearArray(array){
		dataset = array;
		console.log("Llego la informacion");	
		if(switchFirstTime==true){
			console.log("es verdad");
			createFirstTimeGraph();
		}
		else{
			updateGraphstoDay();
		}
	}

	
	
	
function createFirstTimeGraph(){
//Definición de variables de tamaño, colores, estilos
var width = 1000,
    height = 500,
	grosorLinea = 0.5,
	radioCiudades = 4,
	colorPuntoOrigen = "#F20057",
	colorLineaOrigenAccidente = "#F20057",
	colorPuntoAccidente="#EF609A",
	colorPuntoDestino="#EF8FB7",
	colorLineaAccidenteDestino="#EF609A";

var projection = d3.geo.mercator()
    .center([0, 20 ])
    .scale(160)
    .rotate([-3,0]);

var svg = d3.select("body #mapa").append("svg")
    .attr("width", width)
    .attr("height", height);

var path = d3.geo.path()
    .projection(projection);
	
//los grupos que creo en el svg para los difernetes puntos y lineas
var g = svg.append("g").attr("class","puntoOrigen");;
var g2 = svg.append("g").attr("class","puntoDestino");
var g3 = svg.append("g").attr("class","puntoAccidente");
var g4 = svg.append("g").attr("class","lineaVuelo");
var g5 = svg.append("g").attr("class","lineaVuelo");

// load and display the World
d3.json("topology", function(error, topology) {

// load and display the cities and connections

	//Dibujar los puntos de ciudades de origen
    g.selectAll("circle")
       .data(dataset)
       .enter()
       .append("circle")
       .attr("cx", function(d) {
               return projection([d.lonOrigen, d.latOrigen])[0];
       })
       .attr("cy", function(d) {
               return projection([d.lonOrigen, d.latOrigen])[1];
       })
       .attr("r", radioCiudades)
       .style("fill", colorPuntoOrigen)
	   .call(d3.helper.tooltip(
        function(d, i){
          return	"<div class='infoFlight'><b class='tootltipResaltado'>From: " + d.cityOrigen + "</b><br>"+		  			
					"<b>Crash place: "+d.cityAccidente+ "</b><br>"+
					"<b>To: </b>" + d.cityDestino + "</div><br>"+
					"<b>Date: </b>" + d.Date + "<br>"+
					"<b>Hour: </b>" + d.Time+ "<br>"+
					"<b>Pepole Aboard: </b>" + d.Aboard+ "<br>"+
					"<b>Fatalities: </b>" + d.Fatalities+ "<br>"+
					"<b>Fatalities on ground: </b>" + d.Ground+ "<br>"+
					"<b>Summary: </b>" + d.Summary+ "<br>";
        }
        ));
	 //Dibujar los puntos de ciudades de accidente
	 g2.selectAll("circle")
       .data(dataset)
       .enter()
       .append("circle")
       .attr("cx", function(d) {
               return projection([d.lonAccidente, d.latAccidente])[0];
       })
       .attr("cy", function(d) {
               return projection([d.lonAccidente, d.latAccidente])[1];
       })
       .attr("r", radioCiudades)
       .style("fill", colorPuntoAccidente)
	   .call(d3.helper.tooltip(
        function(d, i){
          return	"<div class='infoFlight'><b>From: </b>" + d.cityOrigen + "<br>"+
		  			"<b class='tootltipResaltado'>Crash place: "+d.cityAccidente+ "</b><br>"+
		  			"<b>To: </b>" + d.cityDestino + "<br></div><br>"+					
					"<b>Date: </b>" + d.Date + "<br>"+
					"<b>Hour: </b>" + d.Time+ "<br>"+
					"<b>Pepole Aboard: </b>" + d.Aboard+ "<br>"+
					"<b>Fatalities: </b>" + d.Fatalities+ "<br>"+
					"<b>Fatalities on ground: </b>" + d.Ground+ "<br>"+
					"<b>Summary: </b>" + d.Summary+ "<br>";
  
        }
        ));
		//Dibujar los puntos de ciudades de destino
	  g3.selectAll("circle")
       .data(dataset)
       .enter()
       .append("circle")
       .attr("cx", function(d) {
               return projection([d.lonDestino, d.latDestino])[0];
       })
       .attr("cy", function(d) {
               return projection([d.lonDestino, d.latDestino])[1];
       })
       .attr("r", radioCiudades)
       .style("fill", colorPuntoDestino)
	   .call(d3.helper.tooltip(
        function(d, i){
          return	"<div class='infoFlight'><b>From: </b>" + d.cityOrigen + "<br>"+
		  			"<b>Crash place: "+d.cityAccidente+ "</b><br>"+
		  			"<b class='tootltipResaltado'>To: " + d.cityDestino + "</b><br></div><br>"+					
					"<b>Date: </b>" + d.Date + "<br>"+
					"<b>Hour: </b>" + d.Time+ "<br>"+
					"<b>Pepole Aboard: </b>" + d.Aboard+ "<br>"+
					"<b>Fatalities: </b>" + d.Fatalities+ "<br>"+
					"<b>Fatalities on ground: </b>" + d.Ground+ "<br>"+
					"<b>Summary: </b>" + d.Summary+ "<br>";
        }
        ));
	   //Dibujar la linea de origen accidente
	   g4.selectAll("line")
       .data(dataset)
       .enter()
       .append("line")
       .attr("x1", function(d) {
               return projection([d.lonOrigen, d.latOrigen])[0];
       })
       .attr("y1", function(d) {
               return projection([d.lonOrigen, d.latOrigen])[1];
       })
	   .attr("x2", function(d) {
               return projection([d.lonAccidente, d.latAccidente])[0];
       })
       .attr("y2", function(d) {
               return projection([d.lonAccidente, d.latAccidente])[1];
       })
       .attr("stroke-width", grosorLinea)
	    .attr("stroke", colorLineaOrigenAccidente);
		
		//Dibujar la linea de accidente destino
		g5.selectAll("line")
       .data(dataset)
       .enter()
       .append("line")
       .attr("x1", function(d) {
               return projection([d.lonAccidente, d.latAccidente])[0];
       })
       .attr("y1", function(d) {
               return projection([d.lonAccidente, d.latAccidente])[1];
       })
	   .attr("x2", function(d) {
               return projection([d.lonDestino, d.latDestino])[0];
       })
       .attr("y2", function(d) {
               return projection([d.lonDestino, d.latDestino])[1];
       })
       .attr("stroke-width", grosorLinea)
	    .attr("stroke", colorLineaAccidenteDestino);
	   
	   
     
    /* Esto es para pintar el texto sobre origen, pero dado que van a ser muchos, mejor no por ahora
		g.selectAll("text")
       .data(data)
       .enter()
     .append("text") // append text
       .attr("x", function(d) {
               return projection([d.lonOrigen, d.latOrigen])[0];
       })
       .attr("y", function(d) {
               return projection([d.lonOrigen, d.latOrigen])[1];
       })
       .attr("dy", -7) // set y position of bottom of text
      .style("fill", "black") // fill the text with the colour black
      .attr("text-anchor", "middle") // set anchor y justification
      .text(function(d) {return d.cityOrigen;}); // define the text to display*/



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

	g4.attr("transform","translate("+ 
            d3.event.translate.join(",")+")scale("+d3.event.scale+")");
        g4.selectAll("circle")
            .attr("d", path.projection(projection));
        g4.selectAll("path")  
            .attr("d", path.projection(projection)); 
			
	g5.attr("transform","translate("+ 
            d3.event.translate.join(",")+")scale("+d3.event.scale+")");
        g5.selectAll("circle")
            .attr("d", path.projection(projection));
        g5.selectAll("path")  
            .attr("d", path.projection(projection)); 
    

  });

svg.call(zoom)
	 
}
			
		
				
function updateGraphstoDay(){
	
}
