import smtplib

from email.mime.text import MIMEText

def mail(text, from_addr, to_addr, subject):
  msg = MIMEText(text,'plain')

  msg['Subject'] = subject
  msg['From'] = from_addr
  msg['To'] = to_addr

  # Send the message via our own SMTP server, but don't include the
  # envelope header.
  s = smtplib.SMTP('localhost')
  s.sendmail(from_addr, [to_addr], msg.as_string())
  s.quit()

if __name__ == "__main__":
  text = 'Wie dit leest is gek'
  from_addr = 'error@nagazuka.nl'
  to_addr = 's.anoep@gmail.com'
  subject = 'Boo!'
  mail(text, from_addr, to_addr, subject)
