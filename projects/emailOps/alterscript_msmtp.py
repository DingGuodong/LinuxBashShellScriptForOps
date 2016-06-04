import smtplib
import string

EMAIL_HOST = "smtp.exmail.qq.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = 'noreply@huntor.cn'
EMAIL_HOST_PASSWORD = 'huntor_nor_123'
DEFAULT_FROM_EMAIL = 'noreply@huntor.cn'
CRLF = "\r\n"  # for Windows user

EMAIL_TO = "dinggd@huntor.cn"  # user defined variable
SUBJECT = "Test email from Python"  # user defined variable
text = "Python rules them all!"  # user defined variable
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
