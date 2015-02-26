#!/usr/bin/env python3

import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import argparse
import sys

DEFAULT_FROM = "service@ubu19.ch"
DEFAULT_SUBJECT = "Service Alert."
## Options
parser = argparse.ArgumentParser()
parser.add_argument("-f","--origin",help="From header. Default is %s" % DEFAULT_FROM,default=DEFAULT_FROM)
parser.add_argument("destination",help="Destination email")
parser.add_argument("-i","--image",help="Embed the image denoted by FILE_NAME into the mail. After the text it receives.",default=None)
parser.add_argument("-s","--subject",help="Give a subject to your mail.Default is %s" % DEFAULT_SUBJECT,default = DEFAULT_SUBJECT,required=True)
parser.add_argument("--footer",help="Footer at the end of the mail.")
argss = parser.parse_args()

## read the message
text = sys.stdin.read() 

msgRoot = MIMEMultipart('related')
msgRoot['From'] = argss.origin
msgRoot['Subject'] = argss.subject
msgRoot['To'] = argss.destination
msgRoot.preamble = "This is a multipart message in MIME format"

## create an alternative so client can decide which one to display
msgAlt = MIMEMultipart('alternative')
msgRoot.attach(msgAlt)

## Alternative text message first containing only the text
msgText = MIMEText(text + "\n" + argss.footer)
msgAlt.attach(msgText)
## Or with the image if present
if argss.image is not None:
    msgText = MIMEText("<p>" + text + "</p>" + '<p><h3 style="">Graph</h3><img style="display:block;margin-left:auto;margin-right:auto;" src="cid:image1"></p>' + argss.footer,'html')
    msgAlt.attach(msgText)
    with open(argss.image,"rb") as fp:
        msgImage = MIMEImage(fp.read())
        msgImage.add_header('Content-ID','<image1>')
        msgRoot.attach(msgImage)

smtp = smtplib.SMTP('localhost')
smtp.sendmail(argss.origin,argss.destination,msgRoot.as_string())
smtp.quit()
exit(0)



