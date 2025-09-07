import pypdf as pdf
from pathlib import Path

# Task
# Extract the page that contains Practice Questions from the Recursion.pdf file
# Save this page and rename as Practice_Questions.pdf

def extract_questions(input_file, output_file):
    if not Path(input_file).exists():
        raise FileNotFoundError('Error: file not found')
    if Path(input_file).suffix.lower() != '.pdf':
        print('Only pdf extensions are allowed')
        return False
    try:
        reader = pdf.PdfReader(input_file)
        pdf_pages = reader.pages
        writer = pdf.PdfWriter()
        page_length = len(pdf_pages)
        for page in range(page_length):
            selected_pages = pdf_pages[page]
            keyword = 'Practice Questions'
            if keyword in selected_pages.extract_text():
                writer.add_page(selected_pages)
                with open(output_file, 'wb') as file:
                    writer.write(file)
                print(f'File successfully extracted from page number_{page + 1}')
                return True
        print(f'{keyword} not in other pages')
        return False
    
    except Exception as e:
        print(f'Something went wrong: {e}')

if __name__ == '__main__':
    input_file = 'Recursion.pdf'
    output_file = 'Practice_Questions.pdf'
    extract_questions(input_file, output_file)