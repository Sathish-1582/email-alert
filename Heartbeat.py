import requests
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Email configuration
SMTP_SERVER = 'smtp.bodhee.io'
SMTP_PORT = 587
SMTP_USER = 'support@bodhee.io'
SMTP_PASSWORD = 'DMtqhHuZ7zrH!'
EMAIL_FROM = 'support@bodhee.io'
EMAIL_TO = ['rahul.baliga@neewee.ai', 'somu.sekhar@neewee.ai', 'customeroperations@neewee.ai']

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def send_email(subject, body, recipients):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_FROM, recipients, text)
        server.quit()
        print(f"Email sent successfully to {recipients} with subject: {subject}")
    except Exception as e:
        print(f"[{get_timestamp()}] Failed to send email: {e}")
 def check_heartbeat(url, headers, max_retries=7, retry_delay=5):
    try_count = 0
    final_response = None

    while try_count < max_retries:
        try:
            response = requests.get(url, headers=headers)
            print(f"[{get_timestamp()}] Heartbeat check response {response.status_code}")
            if response.status_code == 200:
                print(f"[{get_timestamp()}] {url} is up and running.")
                break
            else:
                try_count += 1
                time.sleep(retry_delay)
        except Exception as e:
            print(f"[{get_timestamp()}] Error: {e}")
            try_count += 1
            time.sleep(retry_delay)

    if try_count >= max_retries:
        print(f"[{get_timestamp()}] Max retries reached. Heartbeat check failed.")
        send_email(
            subject="Heartbeat Check Failed",
            body=f"Heartbeat check failed after {max_retries} attempts for URL: {url}",
            recipients=EMAIL_TO
        )

    return final_response

if __name__ == "__main__":
    url = "https://bps.gsk.com/wavre/trd-staging/apigateway/api/imp/"
    headers = {"X-Auth-Token": "ffa3f736-41be-4a60-84a9-6c3cd55c2f3a"}
    check_heartbeat(url, headers

