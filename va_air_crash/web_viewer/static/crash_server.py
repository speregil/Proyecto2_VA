import tornado.ioloop
import tornado.web
import os
import pandas as pd
import json
#from geopy.geocoders import Nominatim

#geolocator = Nominatim()
topology = None


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
        
class TrimestreHandler(tornado.web.RequestHandler):
    def get(self):
        df = self.df
        trimestre = self.get_argument("trimestre")
        df_datos = filtro_trimestre(trimestre, df)
        dic = df_datos.to_dict("record")
        self.write({"array":dic})
        
    
    def initialize(self, df):
        self.df = df
    
class OrigenHandler(tornado.web.RequestHandler):
    def get(self):
        df = self.df
        minimo = self.get_argument("minimo")
        maximo = self.get_argument("maximo")
        df_datos = filtro_ciudades_origen(minimo, maximo, df)
        dic = df_datos.to_dict("record")
        self.write({"array":dic})
        
    
    def initialize(self, df):
        self.df = df
        
class DestinoHandler(tornado.web.RequestHandler):
    def get(self):
        df = self.df
        minimo = self.get_argument("minimo")
        maximo = self.get_argument("maximo")
        df_datos = filtro_ciudades_destino(minimo, maximo, df)
        dic = df_datos.to_dict("record")
        self.write({"array":dic})
        
    
    def initialize(self, df):
        self.df = df
        
class AereolineaHandler(tornado.web.RequestHandler):
    def get(self):
        df = self.df
        minimo = self.get_argument("minimo")
        maximo = self.get_argument("maximo")
        df_datos = filtro_aerolineas(minimo, maximo, df)
        dic = df_datos.to_dict("record")
        self.write({"array":dic})
        
    
    def initialize(self, df):
        self.df = df
        
class YearHandler(tornado.web.RequestHandler):
    def get(self):
        df = self.df
        minimo = self.get_argument("minimo")
        maximo = self.get_argument("maximo")
        df_datos = filtro_anios(minimo, maximo, df)
        dic = df_datos.to_dict("record")
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
        
    return list_data

def cuantos_ciudad(ciudad, df):
    df_gets = df.loc[df['Location'].str.contains(ciudad)]
    return df_gets
    
def filtro_trimestre(trimestre, df):
    mesInicial = 0
    mesFinal = 0
    if(trimestre == '1'):
        mesInicial = 1
        mesFinal = 3
    elif(trimestre == '2'):
        mesInicial = 4
        mesFinal = 6
    elif(trimestre == '3'):
        mesInicial = 7
        mesFinal = 9
    elif(trimestre == '4'):
        mesInicial = 10
        mesFinal = 12
    elif(trimestre == '0'):
        mesInicial = 1
        mesFinal = 12
        
    df_tri = df.loc[(df["time"].dt.month >= mesInicial) & (df["time"].dt.month <= mesFinal)]
    df_final = pd.DataFrame(columns=('cityOrigen', 'latOrigen', 'lonOrigen', 'cityDestino', 'latDestino',
                        'lonDestino', 'cityAccidente', 'latAccidente', 'lonAccidente', 'Date',
                        'Type', 'Aboard', 'Fatalities', 'Ground', 'Operator'))
    for i in df_tri.index.values.tolist():
        df_final.loc[len(df_final)+1]=[df_tri['cityOrigen'][i], df_tri['latOrigen'][i], df_tri['lonOrigen'][i],
                                  df_tri['cityDestino'][i], df_tri['latDestino'][i], df_tri['lonDestino'][i],
                                  df_tri['cityAccidente'][i], df_tri['latAccidente'][i], df_tri['lonAccidente'][i],
                                  df_tri[df.columns[0]][i], df_tri['Type'][i], df_tri['Aboard'][i],
                                  df_tri['Fatalities'][i], df_tri['Ground'][i], df_tri['Operator'][i]]
    return df_final

def filtro_ciudades_origen(minimo, maximo, df):
    minimo = int(minimo)
    maximo = int(maximo)
    list_cities = df["cityOrigen"].drop_duplicates().tolist()
    list_count = df.groupby("cityOrigen")["cityOrigen"].count().tolist()
    list_pair = zip(sorted(list_cities), list_count)
    results = [t[0] for t in list_pair if (t[1] >= minimo) & (t[1] <= maximo)]
    
    df_crashes = df.loc[df["cityOrigen"].isin(results)]
    
    df_final = pd.DataFrame(columns=('cityOrigen', 'latOrigen', 'lonOrigen', 'cityDestino', 'latDestino',
                            'lonDestino', 'cityAccidente', 'latAccidente', 'lonAccidente', 'Date',
                            'Type', 'Aboard', 'Fatalities', 'Ground', 'Operator'))
    for i in df_crashes.index.values.tolist():
            df_final.loc[len(df_final)+1]=[df_crashes['cityOrigen'][i], df_crashes['latOrigen'][i], df_crashes['lonOrigen'][i],
                                      df_crashes['cityDestino'][i], df_crashes['latDestino'][i], df_crashes['lonDestino'][i],
                                      df_crashes['cityAccidente'][i], df_crashes['latAccidente'][i], df_crashes['lonAccidente'][i],
                                      df_crashes[df.columns[0]][i], df_crashes['Type'][i], df_crashes['Aboard'][i],
                                      df_crashes['Fatalities'][i], df_crashes['Ground'][i], df_crashes['Operator'][i]]
    
    return df_final
    
def filtro_ciudades_destino(minimo, maximo, df):
    minimo = int(minimo)
    maximo = int(maximo)
    list_cities = df["cityDestino"].drop_duplicates().tolist()
    list_count = df.groupby("cityDestino")["cityDestino"].count().tolist()
    list_pair = zip(sorted(list_cities), list_count)
    results = [t[0] for t in list_pair if (t[1] >= minimo) & (t[1] <= maximo)]
    
    df_crashes = df.loc[df["cityDestino"].isin(results)]
    
    df_final = pd.DataFrame(columns=('cityOrigen', 'latOrigen', 'lonOrigen', 'cityDestino', 'latDestino',
                            'lonDestino', 'cityAccidente', 'latAccidente', 'lonAccidente', 'Date',
                            'Type', 'Aboard', 'Fatalities', 'Ground', 'Operator'))
    for i in df_crashes.index.values.tolist():
            df_final.loc[len(df_final)+1]=[df_crashes['cityOrigen'][i], df_crashes['latOrigen'][i], df_crashes['lonOrigen'][i],
                                      df_crashes['cityDestino'][i], df_crashes['latDestino'][i], df_crashes['lonDestino'][i],
                                      df_crashes['cityAccidente'][i], df_crashes['latAccidente'][i], df_crashes['lonAccidente'][i],
                                      df_crashes[df.columns[0]][i], df_crashes['Type'][i], df_crashes['Aboard'][i],
                                      df_crashes['Fatalities'][i], df_crashes['Ground'][i], df_crashes['Operator'][i]]
    
    return df_final
    
def filtro_aerolineas(minimo, maximo, df):
    minimo = int(minimo)
    maximo = int(maximo)
    list_airlines = df["Operator"].drop_duplicates().tolist()
    list_count = df.groupby("Operator")["Operator"].count().tolist()
    list_pair = zip(sorted(list_airlines), list_count)
    results = [t[0] for t in list_pair if (t[1] >= minimo) & (t[1] <= maximo)]
    
    df_crashes = df.loc[df["Operator"].isin(results)]
    
    df_final = pd.DataFrame(columns=('cityOrigen', 'latOrigen', 'lonOrigen', 'cityDestino', 'latDestino',
                            'lonDestino', 'cityAccidente', 'latAccidente', 'lonAccidente', 'Date',
                            'Type', 'Aboard', 'Fatalities', 'Ground', 'Operator'))
    for i in df_crashes.index.values.tolist():
            df_final.loc[len(df_final)+1]=[df_crashes['cityOrigen'][i], df_crashes['latOrigen'][i], df_crashes['lonOrigen'][i],
                                      df_crashes['cityDestino'][i], df_crashes['latDestino'][i], df_crashes['lonDestino'][i],
                                      df_crashes['cityAccidente'][i], df_crashes['latAccidente'][i], df_crashes['lonAccidente'][i],
                                      df_crashes[df.columns[0]][i], df_crashes['Type'][i], df_crashes['Aboard'][i],
                                      df_crashes['Fatalities'][i], df_crashes['Ground'][i], df_crashes['Operator'][i]]
    
    return df_final
    
def filtro_anios(minimo, maximo, df):
    minimo = int(minimo)
    maximo = int(maximo)
    df_crashes = df.loc[(df["Date"].dt.year >= 2009 - maximo ) & (df["Date"].dt.year <= 2009 - minimo)]
    df_final = pd.DataFrame(columns=('cityOrigen', 'latOrigen', 'lonOrigen', 'cityDestino', 'latDestino',
                        'lonDestino', 'cityAccidente', 'latAccidente', 'lonAccidente', 'Date',
                        'Type', 'Aboard', 'Fatalities', 'Ground', 'Operator'))
    for i in df_crashes.index.values.tolist():
        df_final.loc[len(df_final)+1]=[df_crashes['cityOrigen'][i], df_crashes['latOrigen'][i], df_crashes['lonOrigen'][i],
                                  df_crashes['cityDestino'][i], df_crashes['latDestino'][i], df_crashes['lonDestino'][i],
                                  df_crashes['cityAccidente'][i], df_crashes['latAccidente'][i], df_crashes['lonAccidente'][i],
                                  df_crashes['Date'[i], df_crashes['Type'][i], df_crashes['Aboard'][i],
                                  df_crashes['Fatalities'][i], df_crashes['Ground'][i], df_crashes['Operator'][i]]]
    return df_final
    
if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), "../../../Datos2utf8-2.csv")
    print("Iniciando...")
    print("Cargando Datos...")
    df = pd.read_csv(path)
    
    print("Dandole formato a los datos...")
    df.rename(columns={'OrigenCiudad': 'cityOrigen', 'OrigenLatitud': 'latOrigen', 'OrigenLongitud': 'lonOrigen',
                  'DestinoCiudad': 'cityDestino', 'DestinoLatitud': 'latDestino', 'DestinoLongitud': 'lonDestino',
                  'CrashCiudad': 'cityAccidente', 'CrashPais': 'countryAccidente', 'CrashLatitud': 'latAccidente',
                  'CrashLongitud': 'lonAccidente'}, inplace=True)

    df["time"] = pd.to_datetime(df[df.columns[0]], format="%m/%d/%Y")
    
    print("Cargando Topologia")
    with open("world-110m2.json") as json_file:
        topology = json.load(json_file)
        
    
    
    
    #df["time"] = pd.to_datetime(df.Timestamp, format="%Y-%m-%d %H:%M:%S")
    
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/inicio", InicioHandler, {"df":df}),
        (r"/ciudad", CuantosCiudadHandler, {"df":df}),
        (r"/trimestre", TrimestreHandler, {"df":df}),
        (r"/origen", OrigenHandler, {"df":df}),
        (r"/destino", DestinoHandler, {"df":df}),
        (r"/aereolinea", AereolineaHandler, {"df":df}),
        (r"/anio", YearHandler, {"df":df}),
        (r"/topology", TopologyHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler,
            {"path": settings["static_path"]})

    ], **settings)
    application.listen(8100)
    print("Listo")
    tornado.ioloop.IOLoop.current().start()
