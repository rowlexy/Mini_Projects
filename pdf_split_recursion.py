import pypdf as pdf
from pathlib import Path
import shutil

current_dir = Path.cwd()
folder_path = current_dir/'pdf_folder'
Path.mkdir('pdf_folder', exist_ok=True)

def split_recursion(input_file):
    try:
        reader = pdf.PdfReader(input_file)
        pdf_pages = reader.pages
        page_length = len(pdf_pages)
        for page_num in range(page_length):
            writer = pdf.PdfWriter()
            selected_page = pdf_pages[page_num]
            writer.add_page(selected_page)
            with open(f'Extract_{page_num +1}.pdf', 'wb') as file:
                writer.write(file)
        print(f'Files successfully extracted, total pages: {page_length}')
    except Exception as e:
        print(f'Something went wrong: {e}')
        
split_recursion('Recursion.pdf')

def move_recursion_files():
    for file in current_dir.iterdir():
        if file.stem.startswith('Extract_'):
           shutil.move(file, str(folder_path/file.name))
move_recursion_files()         