import tornado.ioloop
import tornado.web
import generator
import json

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        template = self.get_argument('template', '')
        profile = self.get_argument('profile', '')
        profDict = json.loads(profile)
        print('template %s' % template)
        filename = generator.generate(profDict)
        self.write(filename)

application = tornado.web.Application([
    (r"/generate", MainHandler),
])

if __name__ == "__main__":
    application.listen(18080)
    tornado.ioloop.IOLoop.instance().start()

