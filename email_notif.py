
# Import smtplib for the actual sending function
import smtplib
import os
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
##with open(textfile, 'rb') as fp:
    # Create a text/plain message
##    msg = MIMEText(fp.read())

def send_mail(you, subject, message, task_name):
  me = 'nitinjain0455@gmail.com'
  msg = MIMEMultipart('alternative')
  msg['Subject'] = subject
  msg['From'] = me
  msg['To'] = you


  html = """\
  <html>
    <head></head>
    <body>
      <p>"""+message.format(task_name)+"""<br><br>
        Regards,<br>
        Team Simplii<br><br><br>
        <i>This is an automated email. Please do not respond to this email.</i>
      </p>
    </body>
  </html>
  """

  # Record the MIME types of both parts - text/plain and text/html.
  msg.attach(MIMEText(html, 'html'))

  # Send the message via our own SMTP server, but don't include the
  # envelope header.
  mail = smtplib.SMTP('smtp.gmail.com', 587)
  mail.ehlo()

  mail.starttls()

  # CHANGE IT THE EMAIL CREDENTIALS YOU WANT TO SEND OUT YOUR SIMPLII ALERTS FROM
  mail.login('xyz@gmail.com', '####')
  mail.sendmail(me, you, msg.as_string())
  mail.quit()
  return 