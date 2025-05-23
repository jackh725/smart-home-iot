import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

def send_alert_email(alert_type, timestamp, distance, light):
    try:
        subject = f"[SMART HOME ALERT] {alert_type.upper()}"
        body = f"""
        Alert triggered at {timestamp}.

        Alert Type :{alert_type}
        Distance : {distance} cm
        Light: {light}
        """
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_TO
        msg['Subject'] = subject
        msg.attach(MIMEText(body,'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER,EMAIL_PASS)
            server.send_message(msg)

        print("Emailsent.")
    except Exception as e:
        print("Email send error: ", e)