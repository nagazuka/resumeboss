#!python
import logging
import tornado.ioloop
import tornado.web
import generator
import mail
import json
import traceback

class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        template_name = self.get_argument('template', '')
        profile = self.get_argument('profile', '')
        try:
          profDict = json.loads(profile)
          filename = generator.generate(profDict, template_name, callback=self.on_generate)
        except Exception as e:
          text = "Error occurred during processing:\n%s\nStacktrace:\n" % e
          text = text + traceback.format_exc()
          to_addr = "s.anoep@gmail.com"
          from_addr = "tornado-resumeboss@nagazuka.nl"
          subject = "[ResumeBoss] [ERROR] Unexpected error"
          mail.mail(text, from_addr, to_addr, subject)
          raise

    def on_generate(self, filename):
        self.write(filename)
        self.finish()

application = tornado.web.Application([
    (r"/generate", MainHandler),
], debug=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s %(levelname)s %(message)s')
    logging.info("ResumeBoss server started.")
    application.listen(18080)
    tornado.ioloop.IOLoop.instance().start()
