import pandas as pd

# Load the existing and new data from Excel sheets
existing_data = pd.read_excel('students_4.xlsx')
new_data = pd.read_excel('students_5.xlsx')

# Merge the DataFrames based on 'Roll No'
# You can specify how='inner', 'outer', 'left', or 'right' depending on your needs
merged_data = pd.merge(existing_data, new_data, on='Roll No',
                       how='outer', suffixes=('_old', '_new'))

# Save the merged DataFrame to a new Excel file
merged_data.to_excel('merged_file.xlsx', index=False)
