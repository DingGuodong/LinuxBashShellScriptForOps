import smtplib
from email.mime.text import MIMEText

EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_HOST_USER = 'noreply@example.com'
EMAIL_HOST_PASSWORD = 'my_password'
DEFAULT_FROM_EMAIL = 'noreply@example.com'
EMAIL_TO = 'dinggd@example.com'
EMAIL_MESSAGE_SUBJECT = ''
EMAIL_MESSAGE_CONTENT = ''
msg = MIMEText(EMAIL_MESSAGE_CONTENT, _charset='utf-8')
msg['Subject'] = EMAIL_MESSAGE_SUBJECT
msg['From'] = DEFAULT_FROM_EMAIL
msg['To'] = EMAIL_TO
o = smtplib.SMTP(host=EMAIL_HOST, port=EMAIL_PORT)
o.set_debuglevel(1)
o.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
o.sendmail(DEFAULT_FROM_EMAIL, EMAIL_TO, msg.as_string())
o.quit()
