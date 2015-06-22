/**
 * Script que se encarga de dibujar el mapa incial de la aplicación
 */
accidentes_por_ciudad("Paris")

function mapaInicial() {        				
    console.log("Leyendo los datos...");        
    d3.json("inicio", function (e, d) {
		console.log(d.array);
        });	
}

function accidentes_por_ciudad(ciudad){
	console.log("Buscando datos de " + ciudad + "...");
	var url = "ciudad?"+
				"ciudad="+ciudad;
	d3.json(url, function (e, d) {
		console.log(d.array);
        });	
}