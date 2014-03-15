import os.path
import tornado.ioloop
import tornado.web
import serial
import time, datetime, pytz

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        # Serial Setup
		try:
			serialConnection = serial.Serial('/dev/ttyAMA0', 9600, timeout = 1)
		except:
			print "ERROR: cannot connect to serial port"
		else:
			print "Connection to Serial Port ok"
		
		# open serial connection and readline
		serialConnection = serial.Serial('/dev/ttyAMA0', 9600, timeout = 1)
		#print "Serial connection established"
		
		# weather format (temp, barotemp, humidity, pressure, altitude)
		weatherMeasurements = ""
		while weatherMeasurements == "":
			weatherMeasurements = serialConnection.readline()
		
		# close serial connection
		serialConnection.close()
		#print "Serial connection closed"
		
		# calcualte time and append to weather data and remove '/r/n' 
		timestamp = datetime.datetime.now(pytz.timezone('US/Central')).strftime('%I:%M %p %A %B %d %Y')
		weatherMeasurements.strip()
		weatherData = []
		weatherData = weatherMeasurements.split(',')
		
		# convert to English measurements (Can't get a new function to work right now)
		englishList = []
		# c to f
		englishList.append(float(weatherData[0]) * 1.8 + 32)
		englishList.append(float(weatherData[1]) * 1.8 + 32)
		englishList.append(weatherData[2])
		# Baro pressure
		englishList.append(weatherData[3])
		# altitude, meters to feet
		englishList.append(float(weatherData[4]) * 3.2808)
		# add timestamp
		englishList.append(timestamp)
		self.render("index.html", weatherMeasurements=englishList)
		

handlers = [
	(r"/images/(.*)",tornado.web.StaticFileHandler, {"path": "/home/pi/server/weather/weather_frontend/images"}),
	(r"/css/(.*)",tornado.web.StaticFileHandler, {"path": "/home/pi/server/weather/weather_frontend/css"}),
	(r"/", MainHandler),
]

settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
)               

application = tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
