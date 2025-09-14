# Loop through all Excel files in a folder, convert them to .csv, and save in a new folder.
from pathlib import Path
import csv, shutil, openpyxl
import pandas as pd

# move the excel files in the current directory to a new folder => excel folder
def move_excel_file():
    current_dir = Path.cwd()
    destination = Path('excel_path')
    destination.mkdir(exist_ok=True)
    files_moved = 0
    for file in current_dir.iterdir():
        if file.suffix == '.xlsx':
            shutil.move(str(file), str(destination/file.name))
            files_moved += 1
    if files_moved > 0:
        print(f'{files_moved} files successfully moved to {destination}')
    else:
        print('No excel file was moved')

# Alternatively using openpyxl with csv

def excel_to_csv_converter(input_folder, output_folder):
    excel_path = Path(input_folder)
    if not excel_path.exists:
        print('Folder path does not exist, please specify the correct folder')
        return False
    converted_counter = 0
    for excel_file in excel_path.iterdir():
        if excel_file.suffix == '.xlsx':
            # load the workbook
            try:
                wb = openpyxl.load_workbook(excel_file)
                ws = wb.active
                # convert the excel file to csv
                csv_filename = excel_file.with_suffix('.csv')
                with open(csv_filename, 'w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    
                    # Write all rows from Excel to csv
                    for row in ws.iter_rows(values_only=True):
                        for cell in row:
                            if cell is not None:
                                csv_writer.writerow(row)
                converted_counter += 1
                print(f'Converted: {excel_file.name} -> {csv_filename.name}')
            except Exception as e:
                print(f'Error converting {excel_file.name}')
    # Create a new directory for the csv files
    csv_folder = Path(output_folder)
    csv_folder.mkdir(exist_ok=True)
    csv_files_moved = 0            
    for csv_file in excel_path.iterdir():
        if csv_file.name.endswith('.csv'):
            shutil.move(str(csv_file), str(csv_folder/csv_file.name))
            csv_files_moved += 1
    if csv_files_moved > 0:
        print(f'{csv_files_moved} files moved to {csv_folder}')
        
        
def csv_file_merge(csv_path, output_file):
    csv_folder = Path(csv_path)
    csv_file_list = []
    for file in csv_folder.iterdir():
        if file.suffix == '.csv':
            # read each csv file
            csv_file = pd.read_csv(file)
            csv_file_list.append(csv_file)
    # Checking for csv files
    if csv_file_list:
        merged_file = pd.concat(csv_file_list, ignore_index=True)
        merged_file.to_csv(output_file, index=False)
        print(f'Successfully merged {len(csv_file_list)} CSV files into merged.csv')
    else:
        print('No CSV files found in csv_folder')
        
    
     

if __name__ == '__main__':
    input_folder = 'excel_path'
    output_folder = 'csv_folder'
    csv_path = 'csv_folder'
    output_file = 'merged.csv'
    excel_to_csv_converter(input_folder, output_folder)
    csv_file_merge(csv_path, output_file)