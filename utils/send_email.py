import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

def send_email(subject, message, to_email, _subtype='html'):

    load_dotenv('.credentials/.env')

    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    print(f'SMTP_USERNAME : {SMTP_USERNAME}')
    print(f'SMTP_PASSWORD : {SMTP_PASSWORD}')


    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT =  465   #587  for TLS; use 465 for SSL
    FROM_EMAIL = SMTP_USERNAME

    msg = MIMEText(message, _subtype=_subtype)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email

    print(f'Message : {msg.as_string()}')

    try:
        # Menggunakan SMTP_SSL untuk koneksi SSL
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, [to_email], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False




