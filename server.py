import tornado.ioloop
import tornado.web
import generator

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        filename = generator.generate()
        self.write(filename)

application = tornado.web.Application([
    (r"/generate", MainHandler),
])

if __name__ == "__main__":
    application.listen(18080)
    tornado.ioloop.IOLoop.instance().start()

