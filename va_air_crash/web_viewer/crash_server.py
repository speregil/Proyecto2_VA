import tornado.ioloop
import tornado.web
import os
import pandas as pd
import numpy as np

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
        
settings = {"template_path" : os.path.dirname(__file__),
            "static_path" : os.path.join(os.path.dirname(__file__),"static"),
            "debug" : True
            } 

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), "../../Crashes.csv")
    #dfSun = pd.read_csv(path)  
    #df["time"] = pd.to_datetime(df.Timestamp, format="%Y-%m-%d %H:%M:%S")
    print("Iniciando...")
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler,
            {"path": settings["static_path"]})

    ], **settings)
    application.listen(8100)
    print("Listo")
    tornado.ioloop.IOLoop.current().start()