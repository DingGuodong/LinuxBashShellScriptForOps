import smtplib
import string
import sys


def usage():
    print("""
    Function: send email to somebody using smtp protocol
    Usage: %s <mailto> <subject> <message body>
    Example: python %s "dinggd@huntor.cn" "Test email from Python" "Python rules them all!"
""") % (__file__, sys.argv[0])
    sys.exit(0)


EMAIL_HOST = "smtp.exmail.qq.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = 'noreply@huntor.cn'
EMAIL_HOST_PASSWORD = 'huntor_nor_123'
DEFAULT_FROM_EMAIL = 'noreply@huntor.cn'
CRLF = "\r\n"  # for Windows user

EMAIL_TO = "dinggd@huntor.cn"  # user defined variable
SUBJECT = "Test email from Python"  # user defined variable
text = "Python rules them all!"  # user defined variable

argc = len(sys.argv)
if not (argc == 1 or argc == 4):
    print("Error: incorrect number of arguments or unrecognized option")
    usage()
if argc == 1:
    pass
else:
    if sys.argv[1] is not None and sys.argv[2] is not None and sys.argv[3] is not None:
        EMAIL_TO = sys.argv[1]
        SUBJECT = sys.argv[2]
        text = sys.argv[3]

BODY = string.join((
    "From: %s" % DEFAULT_FROM_EMAIL,
    "To: %s" % EMAIL_TO,
    "Subject: %s" % SUBJECT,
    "",
    text
), CRLF)

server = smtplib.SMTP()
server.connect(EMAIL_HOST, EMAIL_PORT)
server.starttls()
server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
server.sendmail(DEFAULT_FROM_EMAIL, [EMAIL_TO], BODY)
server.quit()
