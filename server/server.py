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
        additional_info = self.get_argument('additional-info', '')
        try:
          profDict = json.loads(profile)
          addinfo_dict = json.loads(additional_info)
          filename = generator.generate(profDict, addinfo_dict, template_name, callback=self.on_generate)
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

class FeedbackHandler(tornado.web.RequestHandler):
    def post(self):
        email_address = self.get_argument('email_address', '')
        name = self.get_argument('name', '')
        feedback = self.get_argument('feedback', '')
        text = "Name: %s\n" % name
        text = text + "E-mail: %s\n" % email_address
        text = text + "Feedback: %s\n" % feedback
        to_addr = "s.anoep@gmail.com"
        from_addr = "tornado-resumeboss@nagazuka.nl"
        subject = "[ResumeBoss] [INFO] Feedback" 
        mail.mail(text, from_addr, to_addr, subject)
        self.finish()

application = tornado.web.Application([
    (r"/generate", MainHandler),
    (r"/feedback", FeedbackHandler)
], debug=True)

if __name__ == "__main__":
    try:
      logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s %(levelname)s %(message)s')
      logging.info("ResumeBoss server started.")
      application.listen(18080)
      tornado.ioloop.IOLoop.instance().start()
    except Exception as e:
      text = "Error occurred during starting server:\n%s\nStacktrace:\n" % e
      text = text + traceback.format_exc()
      to_addr = "s.anoep@gmail.com"
      from_addr = "tornado-resumeboss@nagazuka.nl"
      subject = "[ResumeBoss] [ERROR] Unexpected error"
      mail.mail(text, from_addr, to_addr, subject)
      raise
