import os, smtplib
from dotenv import load_dotenv
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from pathlib import Path
load_dotenv()

sender = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
recipients = os.getenv('RECIPIENTS')
recipient_list = recipients.split(',')
email_distribution_list = [recipient.strip() for recipient in recipient_list]
SMTP_MAIL = 'smtp.gmail.com'
PORT = 587

def send_email(subject, receiver, body, file_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = ', '.join(receiver)
        msg['cc'] = sender
        msg['Subject'] = subject
        content = MIMEText(body, 'plain')
        msg.attach(content)
        
        # checking if file path exists
        if Path(file_path).exists():
            # Add attachment
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            
            filename = Path(file_path).name
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(part)
        else:
            print('File does not exist, there are no attachments')
        # including the cc in recipient list
        all_recipients = [receiver, sender]
        with smtplib.SMTP(SMTP_MAIL, PORT) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, all_recipients, msg.as_string())
        print('Email successfully sent')
    except Exception as e:
        print(f'Error: Email not sent {e}')
               
if __name__ == '__main__':
    body = "Please find the attached report in the attached"
    receiver = email_distribution_list
    file_path = 'toc.pdf'
    subject = 'Recurson Chapter 1'
    send_email(subject, receiver, body, file_path)