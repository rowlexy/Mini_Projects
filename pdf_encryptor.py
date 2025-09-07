# Extract the first two pages from Recursor.pdf
# Encrypt the file and give a password of recur

import pypdf as pdf
from pathlib import Path

def encrypt_pdf_file(input_file, output_file):
    if not Path(input_file).exists():
        raise FileNotFoundError('File does not exist')
    if Path(input_file).suffix.lower() != '.pdf':
        print('Only pdf extensions are allowed')
        return False
    try:
        reader = pdf.PdfReader(input_file)
        pdf_pages = reader.pages
        required_pages = pdf_pages[:2]
        writer = pdf.PdfWriter()
        if len(required_pages) < 2:
            print(f'PDF only has {len(required_pages)} page(s),  extracting all available page')
        else:
            print('Extracting the first two pages')    
        for page in required_pages:
            writer.add_page(page)
        writer.encrypt('recur')
        with open(output_file, 'wb') as file:
            writer.write(file)
        print('File successfully extracted and encrypted')
        return True
    except (pdf.PdfReadError, pdf.PdfWriteError, PermissionError, OSError) as e:
        print(f'Something went wrong {e}')
    
if __name__ == '__main__':
    input_file = 'Recursion.pdf'
    output_file = 'Encrypted_chapter_1.pdf'
    encrypt_pdf_file(input_file, output_file)