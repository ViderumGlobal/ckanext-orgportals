import logging
import smtplib
from socket import error as socket_error
from email.mime.text import MIMEText

from pylons import config


log = logging.getLogger(__name__)

FROM = config.get('ckanext.orgportals.smtp.mail.from', 'usedata@montroseint.com')
TO = config.get('ckanext.orgportals.smtp.mail.to', '')
SMTP_SERVER = config.get('ckanext.orgportals.smtp.server', 'localhost')
SMTP_USER = config.get('ckanext.orgportals.smtp.user', 'username')
SMTP_PASSWORD = config.get('ckanext.orgportals.smtp.password', 'password')

def send_email(content, subject, to, from_=FROM):

    msg = MIMEText(content,'plain','UTF-8')
    to = TO

    if isinstance(to, basestring):
        to = [to]

    msg['Subject'] = subject
    msg['From'] = from_
    msg['To'] = ','.join(to)

    try:
        s = smtplib.SMTP(SMTP_SERVER)
        s.login(SMTP_USER, SMTP_PASSWORD)
        s.sendmail(from_, to, msg.as_string())
        s.quit()

        return 'Email message was successfully sent.'
    except socket_error:
        log.critical('Could not connect to email server. Have you configured the SMTP settings?')

        return 'An error occured while sending the email. Try again.'
