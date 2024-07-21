import pandas as pd

# Load the existing data
existing_data = pd.read_excel('students_4.xlsx')

# Load the new data with updated values
new_data = pd.read_excel('students_rev.xlsx')

# Merge the existing data with new data based on 'Roll No'
merged_data = pd.merge(existing_data, new_data, on='Roll No',
                       how='left', suffixes=('_old', '_new'))

# Define columns for subject names
subject_columns = [
    col for col in existing_data.columns if col not in ['Roll No', 'SGPA']]

# Update subject names and SGPA only where there is a corresponding entry in the new data
for subject in subject_columns:
    merged_data[subject] = merged_data.apply(
        lambda row: row[subject + '_new'] if pd.notna(
            row[subject + '_new']) else row[subject + '_old'],
        axis=1
    )

# Update SGPA column
merged_data['SGPA'] = merged_data.apply(
    lambda row: row['SGPA_new'] if pd.notna(
        row['SGPA_new']) else row['SGPA_old'],
    axis=1
)

# Drop the redundant columns
drop_columns = [col for col in merged_data.columns if col.endswith(
    '_old') or col.endswith('_new')]
updated_data = merged_data.drop(columns=drop_columns)

# Save the updated data to a new Excel file
updated_data.to_excel('updated_file.xlsx', index=False)
