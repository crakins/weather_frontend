import os.path
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        weatherMeasurements = [55,50,80,1000,500,220]
        self.render("index.html", weatherMeasurements=weatherMeasurements)

handlers = [
	(r"/images/(.*)",tornado.web.StaticFileHandler, {"path": "/home/rakins/sites/weather/images"}),
	(r"/css/(.*)",tornado.web.StaticFileHandler, {"path": "/home/rakins/sites/weather/css"}),
	(r"/", MainHandler),
]

settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
)               

application = tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
