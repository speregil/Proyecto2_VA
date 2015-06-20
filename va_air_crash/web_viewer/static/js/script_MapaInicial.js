/**
 * Script que se encarga de dibujar el mapa incial de la aplicación
 */
mapaInicial()

function mapaInicial() {        				
    console.log("Leyendo los datos...");        
    d3.json("inicio", function (e, d) {
		console.log(d.array);
        });	
}