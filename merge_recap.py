#    * Merge all CSV files into one master file.
#    * Clean null values or invalid rows before saving.
import pandas as pd
from pathlib import Path



def master_file(csv_folder, output_file):
    if not csv_folder.exists():
        print('The path you tried to access does not exist')
        return False
    csv_file_list = []
    for file in csv_folder.iterdir():
        if file.suffix == '.csv':
            try:
                csv_file = pd.read_csv(file) # read each csv files
                csv_file_list.append(csv_file)
                print(f'Loaded: {file.name}')
            except Exception as e:
                print(f'Skipped {file.name}: {e}')
                continue
        
    # check if files are in csv file list
    if csv_file_list:
        #merge the csv files
        merged_csv_file = pd.concat(csv_file_list, ignore_index=True)
        # count rows before removing duplicates
        initial_rows = len(merged_csv_file)
        #clean the null values and invalid rows
        cleaned_csv_file = merged_csv_file.dropna(how='all')
        # remove duplicates
        unique_csv_data = cleaned_csv_file.drop_duplicates()
        # count rows after removing duplicates
        final_rows = len(unique_csv_data)
        # convert merged file to csv
        unique_csv_data.to_csv(output_file, index=False)
        print(f'Successfully merged {len(csv_file_list)} CSV files into {output_file}')
        print(f'Rows before cleaning: {initial_rows}')
        print(f'Rows after cleaning: {final_rows}')
        print(f'Rows removed: {initial_rows - final_rows}')
        return True
    else:
        print('No CSV files found in csv_folder')
        return False
        
if __name__ == '__main__':
    csv_folder = Path('csv_folder')
    output_file = 'masterfile.csv'
    master_file(csv_folder, output_file)
    