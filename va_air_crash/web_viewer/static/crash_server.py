import tornado.ioloop
import tornado.web
import os
import pandas as pd
import json
from geopy.geocoders import Nominatim

geolocator = Nominatim()
data = pd.DataFrame()
topology = None
test = None
template_topo = {
    "city":"NaN",
    "country":"NaN",
    "lat":0,
    "lon":0,
	"cityDestino":"NaN",
    "countryDestino":"NaN",
    "latDestino":-15.67,
    "lonDestino":-47.43,
	"cityAccidente":"NaN",
    "countryAccidente":"NaN",
    "latAccidente":-4.09,
    "lonAccidente":-70.00
  }

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
        
class InicioHandler(tornado.web.RequestHandler):
    def get(self):
        df = self.df
        #list_data = datos_iniciales(df)
        #self.write({"array" :list_data})
        self.write(test)
    
    def initialize(self, df):
        self.df = df

class CuantosCiudadHandler(tornado.web.RequestHandler):
    def get(self):
        df = self.df
        ciudad = self.get_argument("ciudad")
        df_ciudad = cuantos_ciudad(ciudad, df)
        dic = {'ciudad': ciudad, 'count': df_ciudad.shape[0]}
        self.write({"array":dic})
    
    def initialize(self, df):
        self.df = df
        
class TopologyHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(topology)

settings = {"template_path" : os.path.dirname(__file__),
            "static_path" : os.path.join(os.path.dirname(__file__),"static"),
            "debug" : True
            } 

def datos_iniciales(df):
    global template_topo
    locations = df['Location'].drop_duplicates()
    df_small = locations.sample(10)
    list_data = []
    for index in df_small.iteritems():
        try:
            location = geolocator.geocode(index[1])
        except:
            pass
        if(not location is None):
            limpiar_template()
            template_topo["city"] = index[1]
            template_topo["lat"] = location.latitude
            template_topo["lon"] = location.longitude
            list_data.append(template_topo)
    return list_data

def cuantos_ciudad(ciudad, df):
    df_gets = df.loc[df['Location'].str.contains(ciudad)]
    return df_gets

def limpiar_template():
    global template_topo    
    template_topo = {
    "city":"NaN",
    "country":"NaN",
    "lat":0,
    "lon":0,
	"cityDestino":"NaN",
    "countryDestino":"NaN",
    "latDestino":-15.67,
    "lonDestino":-47.43,
	"cityAccidente":"NaN",
    "countryAccidente":"NaN",
    "latAccidente":-4.09,
    "lonAccidente":-70.00
    }
    
if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), "../../../Crashes.csv")
    print("Iniciando...")
    print("Cargando Datos...")
    df = pd.read_csv(path)
    df['Location'].fillna('NaN', inplace=True)
    with open("world-110m2.json") as json_file:
        topology = json.load(json_file)
        
    with open("ciudades.json") as json_file:
        test = json.load(json_file)
    
    
    #df["time"] = pd.to_datetime(df.Timestamp, format="%Y-%m-%d %H:%M:%S")
    
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/inicio", InicioHandler, {"df":df}),
        (r"/ciudad", CuantosCiudadHandler, {"df":df}),
        (r"/topology", TopologyHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler,
            {"path": settings["static_path"]})

    ], **settings)
    application.listen(8100)
    print("Listo")
    tornado.ioloop.IOLoop.current().start()