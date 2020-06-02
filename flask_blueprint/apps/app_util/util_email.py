import os, sys
import argparse

import smtplib
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText

"""
https://www.google.com/settings/security/lesssecureapps
https://accounts.google.com/DisplayUnlockCaptcha
"""

# SERVER = "localhost"
# SERVER_PORT_GMAIL = ('smtp.gmail.com', 587)
# SERVER_PORT_ZOHO = ("smtp.zoho.com", 587) # 465)   SSl

# FROM = "daniel@acrosspond.com"
FROM = "danschoe@gmail.com"

#TO = ["danschoe@gmail.com"]   # must be a list
TO = ['daniel@acrosspond.com']  #["daniel@acrosspond.com"]   # must be a list


def email_smtp(pw, server_port, addr_from, addr_to, msg_subject, msg_body):

    if type(addr_to) is list:   # isinstance(l, list)
        to = ", ".join(addr_to)

    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (addr_from, addr_to, msg_subject, msg_body)

    msg = MIMEMultipart()
    msg['Subject'] = msg_subject
    msg['From'] = addr_from
    msg['To'] = addr_to
    # Record the MIME types of both parts - text/plain and text/html.
    part0 = MIMEText(msg_body, 'plain')
    # part2 = MIMEText(HTML_BODY, 'html')

    msg.preamble = 'The preamble'
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part0)
    # msg.attach(part1)

    server = None
    try:
      server = smtplib.SMTP(server_port[0], server_port[1])

      server.ehlo()
      server.starttls()
      server.ehlo()
      server.login(addr_from, pw)

      failed_addr = server.sendmail(addr_from, addr_to, msg.as_string())

    except:
      print("Error: unable to send email", sys.exc_info()[0])
    finally:
      if server:
          server.quit()


def email_newsletter_tribal(pw, to_lst=None):

    msg_subject = "Hello!"
    msg_body = "This message was sent with Python's smtplib."
    if not to_lst:
        to_lst = TO_LST

    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, msg_content)


    msg = MIMEMultipart()
    msg['Subject'] = msg_subject
    msg['From'] = FROM
    msg['To'] = ", ".join(to_lst)
    # Record the MIME types of both parts - text/plain and text/html.
    part0 = MIMEText(msg_body, 'plain')
    # part2 = MIMEText(HTML_BODY, 'html')

    msg.preamble = 'The preamble'
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part0)
    # msg.attach(part1)

    server = None
    try:
      server = smtplib.SMTP(SERVER_PORT[0], SERVER_PORT[1])

      server.ehlo()
      server.starttls()
      server.ehlo()
      server.login(FROM, pw)

      #failed_addr = server.sendmail(FROM, TO, msg.as_string())
      failed_addr = server.sendmail(FROM, ", ".join(TO), msg.as_string())
    except:
      print("Error: unable to send email", sys.exc_info()[0])
    finally:
      if server:
          server.quit()


def email_sendmail():
    SENDMAIL = "/usr/sbin/sendmail"   # linux sendmail location

    FROM = "sender@example.com"
    TO = ["user@example.com"]

    SUBJECT = "Hello!"

    TEXT = "This message was sent via sendmail."

    # Prepare actual message

    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    # Send the mail
    """
    p = os.popen("%s -t -i" % SENDMAIL, "w")
    p.write(message)
    status = p.close()
    if status:
        print "Sendmail exit status", status

    # The -t option tells sendmail to parse the message, and extract the necessary routing
    # information itself.
    """

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('pw')

    args = parser.parse_args()

    email_smtp(args.pw, msg_subject, msg_body, addr_from, addr_to)
