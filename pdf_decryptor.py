import pypdf as pdf
from pathlib import Path

def decrypt_pdf_file(input_file, output_file, password):
    if not Path(input_file).exists():
        raise FileNotFoundError('File does not exist')
    if Path(input_file).suffix != '.pdf':
        print('Only pdf extensions are allowed')
        return False
    try:
        reader = pdf.PdfReader(input_file)
        pdf_pages = reader.pages
        # Check if PDF is encrypted
        if not reader.is_encrypted:
            print('PDF is not encrypted - no decryption needed')
            return False
        # Try to decrypt with the provided password
        decrypt_success = reader.decrypt(password)
        if not decrypt_success:
            print('Incorrect password - decryption failed')
            return False
        print('Password correct - decrypting PDF...')
        
        writer = pdf.PdfWriter()
        for page in pdf_pages:
           writer.add_page(page)     
        with open(output_file, 'wb') as file:
            writer.write(file)
        print(f'File successfully decrypted and saved as: {output_file}')
        return True
    except (pdf.PdfReadError, pdf.PdfWriteError, PermissionError, OSError) as e:
        print(f'Something went wrong: {e}')
        return False
    
def decrypt_prompt(input_file, output_file):
    import getpass # for secure password input
    try:
        password = getpass.getpass("Enter PDF password: ")
        return decrypt_pdf_file(input_file, output_file, password)
    except KeyboardInterrupt:
        print("\nDecryption cancelled by user")
        return False

if __name__ == '__main__':
    input_file = 'Encrypted_chapter_1.pdf'
    output_file = 'Decrypted_chapter_1.pdf'
    password = 'recur'
    success = decrypt_prompt(input_file, output_file)
    
    if success:
        print("Decryption completed successfully!")
    else:
        print("Decryption failed.")