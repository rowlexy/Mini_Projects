import pypdf as pdf
from pathlib import Path
def decrpyt_tester(input_file, output_file, password):
    if not Path(input_file).exists():
        raise FileNotFoundError('File does not exist')
    if not Path(input_file).suffix != '.pdf':
        print('Only pdf extensions are allowed')
        return False
    # read pdf pages
    try:
        reader = pdf.PdfReader(input_file)
        pdf_pages = reader.pages
        # Check for encryption
        if not reader.is_encrypted:
            print('PDF is not encrypted')
            return False
        # if encrypted, insert the password
        decryption_success = reader.decrypt(password)
        if not decryption_success:
            print('Incorrect password - Decryption failed!')
            return False
        print('Decrypting PDF....')
        writer = pdf.PdfWriter()
        # Save the decrypted pdf into the output file
        for page in pdf_pages:
            writer.add_page(page)
        with open(output_file, 'wb') as file:
            writer.write(file)
    except Exception as e:
        print(f'Something went wrong {e}')
        return False
    
def decrypt_prompt(input_file, output_file):
    import getpass
    try:
        password = getpass.getpass('Enter PDF password: ')
        return decrpyt_tester(input_file, output_file, password)
    except KeyboardInterrupt:
        print('Decryption interrupted by user')
        return False

if __name__ == '__main__':
    input_file = 'Encrypted_chapter_1.pdf'
    output_file = 'Test_decrypt.pdf'
    password = 'recur'
    success = decrypt_prompt(input_file, output_file)    
    if success:
        print('PDF successfully decrypted')
    else:
        print('Decryption Failed')
    