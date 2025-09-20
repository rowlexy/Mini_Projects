from pathlib import Path
from dotenv import load_dotenv
import os, smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()
sender = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
recipients = os.getenv('RECIPIENTS')
names = os.getenv('NAMES')
name_list = names.split(',')
contact_names = [name.strip() for name in name_list]
recipient_list = recipients.split(',')
distribution_list = [email.strip() for email in recipient_list]
SMTP_LINK = 'smtp.gmail.com'
PORT = 587

def send_email(subject, body, contact_email, receiver_name, attachment):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['Subject'] = subject
    msg['To'] = contact_email
    msg['cc'] = sender
    # Personalize the message body with receipient's name
    personalized_body = body.format(name=receiver_name)
    content = MIMEText(personalized_body, 'plain')
    msg.attach(content)
    
    # Checking if there's an attachment
    if Path(attachment).exists():
        with open(attachment, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
        encoders.encode_base64(part)
        
        file_name = Path(attachment).name
        part.add_header('Content-Disposition', f'attachment; filename={file_name}')
        msg.attach(part)
    else:
        print('File does not exist, no attachment found.')
        
    # all_recipients = [contact_email, sender] # not needed, sender's inbox will be flooded if sender is the cc
    with smtplib.SMTP(SMTP_LINK, PORT) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, contact_email, msg.as_string())
        print('Email successfully sent')
        
def send_bulk_personalized_emails(subject, body, attachment):
    # The length of manes must equal length of corresponding email address
    if len(contact_names) != len(distribution_list):
        print(f'Error: Number of names ({len(contact_names)}) does not match number of ({len(distribution_list)})')
        return
    # Send personalized email to each recipient
    for name, email in zip(contact_names, distribution_list):
        try:
            send_email(subject, body, email, name, attachment)
        except Exception as e:
            print(f"Failed to send email to {name} ({email}): {str(e)}")
            
if __name__ == '__main__':
    body = 'Hello {name},\nPlease find notes on Recursion in the attached\nPassword: recur\nBest regards,'
    subject = 'Recursion Chapter 1'
    attachment = 'Encrypted_chapter_1.pdf'
    
    send_bulk_personalized_emails(subject, body, attachment)