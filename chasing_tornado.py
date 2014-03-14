import os.path
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        storm_chasers = ["One", "Two"]
        self.render("index.html", storm_chasers=storm_chasers)

handlers = [
	(r"/", MainHandler),
]

settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
)               

application = tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
