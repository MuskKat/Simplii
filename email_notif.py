
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
##with open(textfile, 'rb') as fp:
    # Create a text/plain message
##    msg = MIMEText(fp.read())

me = 'nitinjain0455@gmail.com'
you = 'muskyk32@gmail.com'
msg = MIMEMultipart('alternative')
msg['Subject'] = 'test file'
msg['From'] = me
msg['To'] = you

text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')
msg.attach(part1)
msg.attach(part2)

# Send the message via our own SMTP server, but don't include the
# envelope header.
mail = smtplib.SMTP('smtp.gmail.com', 587)
mail.ehlo()

mail.starttls()

mail.login('nitinjain0455@gmail.com', 'swjq qzus winm tylx')
mail.sendmail(me, you, msg.as_string())
mail.quit()