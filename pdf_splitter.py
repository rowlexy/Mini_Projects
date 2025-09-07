import pypdf as pdf
from pathlib import Path

# Task
# Extract the page that contains Practice Questions from the Recursion.pdf file
# Save this page and rename as Practice_Questions.pdf
# Print out the page number of the extracted page 

def extract_questions(input_file, output_file):
    if not Path(input_file).exists():
        raise FileNotFoundError('File does not exist')
    if Path(input_file).suffix.lower() != '.pdf':
        print('Only pdf extensions are allowed')
        return False
    try:
        reader = pdf.PdfReader(input_file)
        pdf_pages = reader.pages
        page_length = len(pdf_pages)
        writer = pdf.PdfWriter()
        for page in range(page_length):
            file_page = pdf_pages[page]
            page_text = file_page.extract_text()
            keyword = 'Practice Questions'
            if keyword in page_text:
                writer.add_page(file_page)
                with open(output_file, 'wb') as file:
                    writer.write(file)
                print(f'Page successfully extracted from page number-{page + 1}')
                return True
        print('Page not extracted')
        return False
               
    except Exception as e:
        print(f'Something went wrong: {e}')
    
if __name__ == '__main__':
    input_file = 'Recursion.pdf'
    output_file = 'Practice_Questions.pdf'
    extract_questions(input_file, output_file)
        
        
        
