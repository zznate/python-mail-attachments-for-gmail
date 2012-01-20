# Import smtplib for the actual sending function
import smtplib
import os
from datetime import date
from optparse import OptionParser

# Here are the email package modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

def buildMessage():
    msg = MIMEMultipart()    
    msg['Subject'] = 'Emails for today'
    msg['From'] = 'nate@buildbotdatastax.com'
    msg['To'] = 'nate@datastax.com, matt@datastax.com'
    msg.preample = 'Emails for today'
    return msg;
    
def attachFileToPart():
    fn = '/tmp/communityleads_'+date.today().strftime("%Y%m%d")+'.csv'
    fp = open(fn, 'rb')
    part = MIMEBase('application', "octet-stream")
    part.set_payload( fp.read()  )
    fp.close()

    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(fn))
    return part;

def doTransport(msg, options):    
    # Send the email via our own SMTP server.
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(options.user,options.password)
    s.sendmail('nate@buildbot.datastax.com', [options.recipients.split(',')], msg.as_string())
    s.quit()

def main():
    parser = OptionParser()
    parser.add_option("-u","--user", dest="user", help="Username for the mail account")
    parser.add_option("-p","--password", dest="password", help="Password for the mail account")
    parser.add_option("-r","--recipients", dest="recipients", help="Recipient email addresses (comma separated)")
    (options, args) = parser.parse_args()
    if not options.user or not options.password:
        parser.error("user and password are required")
    if not options.recipients:
        parser.error("At least one recipient must be defined")
    print("args:",options.recipients.split(','))
    msg = buildMessage();
    part = attachFileToPart();
    msg.attach(part)
    doTransport(msg,options);

main()
