import os
from smtplib import SMTP
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart



def send_email(message: str, send_to_email: str, subject: str):
    """used to send an email"""
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = formataddr(("Rally", os.getenv("EMAIL_SENDER")))
    msg['To'] = send_to_email
    msg.attach(MIMEText(message, "html"))

    smtp = SMTP()
    smtp.set_debuglevel(0)
    smtp = SMTP(os.getenv("SMTP_SENDER"), os.getenv("SMTP_PORT"))
    smtp.connect(os.getenv("SMTP_SENDER"), os.getenv("SMTP_PORT"))
    smtp.starttls()
    smtp.login(os.getenv("EMAIL_SENDER"),  os.getenv("EMAIL_PASSWORD"))
    smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
    smtp.quit()
