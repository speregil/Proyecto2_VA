import tornado.ioloop
import tornado.web
import os
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim

geolocator = Nominatim()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
        
class InicioHandler(tornado.web.RequestHandler):
    def get(self):
        df = self.df
        dic = datos_iniciales(df)
        self.write({"array" :dic})
    
    def initialize(self, df):
        self.df = df
        
settings = {"template_path" : os.path.dirname(__file__),
            "static_path" : os.path.join(os.path.dirname(__file__),"static"),
            "debug" : True
            } 

def datos_iniciales(df):
    locations = df['Location'].drop_duplicates()
    df_small = locations.sample(100)
    dic_locations = {}
    lat = []
    lon = []
    nom = []
    for index in df_small.iteritems():
        try:
            location = geolocator.geocode(index[1])
        except:
            pass
        if(not location is None):
            nom.append(index[1])
            lat.append(location.latitude)
            lon.append(location.longitude)
    dic_locations['Location'] = nom
    dic_locations['Latitud'] = lat
    dic_locations['Longitud'] = lon
    return dic_locations

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), "../../Crashes.csv")
    print("Iniciando...")
    print("Cargando Datos...")
    df = pd.read_csv(path)
    #df["time"] = pd.to_datetime(df.Timestamp, format="%Y-%m-%d %H:%M:%S")
    
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/inicio", InicioHandler, {"df":df}),
        (r"/static/(.*)", tornado.web.StaticFileHandler,
            {"path": settings["static_path"]})

    ], **settings)
    application.listen(8100)
    print("Listo")
    tornado.ioloop.IOLoop.current().start()