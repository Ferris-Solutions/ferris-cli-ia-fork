import smtplib

from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid

import jinja2


# Open the plain text file whose name is in textfile for reading.

'''
with open('./test_message.txt') as fp:
    msg = EmailMessage()
    msg.set_content(fp.read())
'''

msg = EmailMessage()
msg.set_content('test abc')

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'test 123'
msg['From'] = 'bal@ballab.com'
msg['To'] = 'bal@ballab.com'

# Send the message via our own SMTP server.
s = smtplib.SMTP('mailhog:1025')

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)

TEMPLATE_FILE = "test_message.jinja"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render()  # this is where to put args to the template renderer

asparagus_cid = make_msgid()
msg.add_alternative(outputText.format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')

s.send_message(msg)
s.quit()