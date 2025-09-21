# PDF → Excel → Email Workflow
# * Extract text from a PDF (say invoice numbers)
# * Store into an Excel file
# * Email the Excel file automatically to yourself.
# * Libraries: pypdf, openpyxl, smtplib

import smtplib, openpyxl, re, os
import pypdf as pdf
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# Extracting 'Invoice #'
invoice_number = [] # initializing empty list to collect the invoice numbers
po_number = [] # initializing empty list to collect the po numbers
invoice_date = [] # initializing empty list to collect the date of invoice
def extract_data_from_pdf(input_pdf):
    if Path(input_pdf).exists():
        if Path(input_pdf).suffix != '.pdf':
            print('Only .pdf extensions are acccepted')
            return False
        try:
            reader = pdf.PdfReader(input_pdf)
            pdf_pages = reader.pages
            months = r'(January|February|March|April|May|June|July|August|September|October|November|December)'
            days = r'(\d{1,2})'
            year = r'(\d{1,4})'
            for page_num in range(len(pdf_pages)):
                page = pdf_pages[page_num]
                # getting the Invoice number match
                inv_match = re.findall(r'Invoice #:\s*([A-Z0-9-]+)', page.extract_text())
                # getting the PO number match
                po_match = re.findall(r'PO Number:\s*([A-Z0-9-]+)', page.extract_text())
                # getting the invoice date match
                inv_date_match = re.findall(rf'Invoice Date:\s*{months}\s+{days},\s+{year}', page.extract_text())
                invoice_number.append(inv_match[0])
                po_number.append(po_match[0])
                invoice_date.append(' '.join(inv_date_match[0]))
            print(f'Data appended to the list: \n{invoice_number} \n{po_number}\n{invoice_date}')
            return True
        except Exception as e:
            print(f'Error: Unable to retrieve data - {e}')
            return False
    else:        
        print('The file you tried to access does not exist')
        return False
    
def convert_pdf_data_to_excel(output_excel):
    try:      
        wb = openpyxl.Workbook() # create a new wokbook
        ws = wb.active
        headers = ['Invoice Number', 'PO Number', 'Date']
        # Appending the headers to the worksheet
        ws.append(headers)
        # We can use invoice_number because it has the same range with Po_number & invoice_date    
        for i, inv_num in enumerate(invoice_number):
            row_num = i + 2
            # Append Invoice numbers here
            ws.cell(row=row_num, column=1, value=inv_num)
            ws.cell(row=row_num, column=2, value=po_number[i])
            ws.cell(row=row_num, column=3, value=invoice_date[i])
        print('Values appended to the cells')
        wb.save(output_excel)
        return True
    except Exception as e:
        print(f'Unable to save files to the worksheet: {e}')
        return False
    
# Add variables from environment
SMTP_LINK = 'smtp.gmail.com'
PORT = 587
sender = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
contact_names = os.getenv('NAMES').split(',')
contact_email_address = os.getenv('NAMES').split(',')

contact_email_list = [email for email in contact_email_address]
contact_name_list = [name for name in contact_names]

def send_email(subject, body, contact_email, contact_name, attachment):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = contact_email
        msg['Subject'] = subject
        # To display individual names of contacts
        personalised_body = body.format(name=contact_name)
        content = MIMEText(personalised_body, 'plain')
        msg.attach(content)
        if Path(attachment).exists():
            file_name = Path(attachment).name
            with open(attachment, 'rb') as file:
                part = MIMEBase('appplication', 'octet-stream')
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={file_name}')
            msg.attach(part)
            print(f'{file_name} successfully attached')
        else:
            print('The file you are trying to access does not exist')
        with smtplib.SMTP(SMTP_LINK, PORT) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, contact_email, msg.as_string())
        print(f'Email successfully sent to {contact_email}')
    except Exception as e:
        print(f'Email not sent to recipient: {e}')

def send_personalised_email(subject, body, attachment):
    try:
        if len(contact_name_list) != len(contact_email_list):
            print(f'Names of contact: {len(contact_name_list)} must be equal to their email addresses: {len(contact_email_list)}')
            return
        for contact_email, contact_name in zip(contact_email_list, contact_name_list):
            send_email(subject, body, contact_email, contact_name, attachment)
    except Exception as e:
        print(f'Error, email not sent to{contact_name}: {e}')        
    
if __name__ == '__main__':
    input_pdf = 'Invoice_Collection.pdf'
    output_excel = 'Invoice_Data.xlsx'
    subject = 'Final Project'
    body = """
    Dear {name},
    Congratulations on completing the project.\n
    Hopefully, you get to keep up with the pace
    
    Kind regards,
    """
    attachment = 'Invoice_Data.xlsx'
    extract_data_from_pdf(input_pdf)
    convert_pdf_data_to_excel(output_excel)
    send_personalised_email(subject, body, attachment)
    




    

    
        