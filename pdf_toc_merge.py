# Merge the individual pdf files in pdf_folder numerically
# Use html to create a table of content that shows the name of the files and page number
# Insert the table of content as first page

import pypdf as pdf
from pathlib import Path

def get_number(x):
    try:
        number = int(x.stem.split('_')[1])
        return number
    except (IndexError, ValueError):
        return 0
def create_toc_html(folder_path, html_file):
    if not folder_path.exists():
        print('The folder path you are trying to access does not exist')
        return False
    # Sort the files
    try:
        pdf_files = [pdf_file for pdf_file in folder_path.iterdir() if pdf_file.suffix == '.pdf']
        sorted_pdf_files = sorted(pdf_files, key=get_number)
        filenames = [file.name for file in sorted_pdf_files]
        print(filenames)

        content = ''
        for i, file_name in enumerate(filenames, 1):
            content += f"""
                        <div class="toc-style">
                            <span>{i}. {file_name}</span><span>Page {i+1}</span> 
                        </div>
                        """
        html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
                <style>
                    @page {{
                        size: A4;
                        margin: 0;
                    }}
                    @media print {{
                            body {{
                                margin: 0;
                                padding: 40px;
                                -webkit-print-color-adjust: exact;
                                print-color-adjust: exact;
                            }}
                            @page {{
                                size: A4;
                                margin: 0;
                            }}
                        }}
                    * {{
                        box-sizing: border-box;
                    }}
                    
                    body {{
                        font-family: Arial, Helvetica, sans-serif;
                        padding: 40px;
                        margin: 0;
                        line-height: 1.5;
                    }}
                    .toc-style {{
                        display: flex;
                        margin: 15px 0;
                        justify-content: space-between;
                        border-bottom: 1px dotted #000;
                        padding-bottom: 10px;
                        font-size: 1rem;
                        padding-bottom: 0.25em;
                    }}
                    h1 {{
                        text-align: center;
                        color: #000; 
                        border-bottom: 2px solid #000; 
                        padding-bottom: 10px; 
                    }}
                </style>
            </head>
            <body>
                <h1>Table of content</h1>
                {content}
            </body>
            </html>
        """
        with open(html_file, 'w', encoding='UTF-8') as file:
            file.write(html)
        print('HTML page saved as index.html')
        print('Follow these steps: \n')
        print('1. Open index.html in your browser')
        print('2. Press Cmd+P or Ctrl+P')
        print('3. Save as PDF') # Save the pdf file as toc.pdf
        print('4. Run the merge function')
    except Exception as e:
        print(f'Something went wrong {e}')
        return False

def merge_html_with_pdf(folder_path, merged_pdf):
    # checking id toc.pdf exists
    toc_path = Path('toc.pdf')
    if not toc_path.exists():
        raise FileNotFoundError('toc.pdf file not found')
    try:
        writer = pdf.PdfWriter()
        toc_reader = pdf.PdfReader('toc.pdf')
        for toc_page in toc_reader.pages:
            writer.add_page(toc_page)
        print('Table of content added')
        # Add other sorted pages to the merged PDF
        pdf_files = sorted(folder_path.glob('*.pdf'), key=get_number)
        for pdf_file in pdf_files:
            reader = pdf.PdfReader(pdf_file)
            for page in reader.pages:
                writer.add_page(page)
        # Save the toc and other pages
        with open(merged_pdf, 'wb') as file:
            writer.write(file)
        print('merged_recursion.pdf created')
    except Exception as e:
        print(f'Something went wrong: {e}')
        return False
    
if __name__ == '__main__':
    try:
        folder_path = Path('pdf_folder')
        html_file = 'index.html'
        merged_pdf = 'merged_recursion.pdf'
        print("Choose an option:")
        print("1. Create HTML file (you convert manually)")
        print("2. Simple merge (if you have toc.pdf ready)")
        choice = input('Enter 1 or 2: ')
        if choice == '1':
            create_toc_html(folder_path, html_file)
        elif choice == '2':
            merge_html_with_pdf(folder_path, merged_pdf)
        else: 
            print('Incorrect choice')
    except KeyboardInterrupt:
        print('Process interrupted by user')

    