import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the results page
url = "https://www.osmania.ac.in/res07/20240527.jsp"

# Define a mapping from grade to grade points
grade_to_points = {
    'S': 10,
    'A': 9,
    'B': 8,
    'C': 7,
    'D': 6,
    'E': 5,
    'F': 4,
}


def get_result_page(roll_number, session):
    data = {
        "htno": str(roll_number),
        "mbstatus": "SEARCH",
        "Submit": "Go"
    }
    response = session.post(url, data=data)
    if response.status_code == 200:
        return response.text
    else:
        return None


def extract_details(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    details = {}

    # Locate the table containing the SGPA
    result_table = soup.find('table', {'id': 'AutoNumber5'})
    if result_table:
        for row in result_table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) > 0:
                text_content = ""
                if len(cells) > 0 and 'PASSED' in cells[0].text:
                    text_content = cells[0].text.strip()
                elif len(cells) > 1 and 'PASSED' in cells[1].text:
                    text_content = cells[1].text.strip()
                elif len(cells) > 2 and 'PASSED' in cells[2].text:
                    text_content = cells[2].text.strip()
                if len(cells) > 0 and 'PROMOTED' in cells[0].text:
                    text_content = cells[0].text.strip()
                elif len(cells) > 1 and 'PROMOTED' in cells[1].text:
                    text_content = cells[1].text.strip()
                elif len(cells) > 2 and 'PROMOTED' in cells[2].text:
                    text_content = cells[2].text.strip()
                if 'PASSED' in text_content:
                    sgpa = text_content.split(
                        '-')[1].strip()  # Extract SGPA value
                    details['SGPA'] = sgpa
                elif 'PROMOTED' in text_content:
                    details['SGPA'] = 'Promoted'
    else:
        print("SGPA Table not found")

    # Locate the table containing the subject details
    marks_table = soup.find('table', {'id': 'AutoNumber4'})
    if marks_table:
        subject_grades = {}
        for row in marks_table.find_all('tr')[1:]:  # Skip header rows
            cells = row.find_all('td')
            if len(cells) > 3:  # Ensure there are enough columns
                sub_code = cells[0].text.strip()
                if sub_code.isdigit() and 500 <= int(sub_code) < 600:
                    subject_name = cells[1].text.strip()
                    if len(cells) > 4:
                        grade_secured = cells[4].text.strip()
                    elif len(cells) > 3:
                        grade_secured = cells[3].text.strip()
                    else:
                        grade_secured = 'N/A'
                    grade_points = grade_to_points.get(grade_secured, 'N/A')
                    # Add the grade secured and grade points to the subject_grades dictionary
                    subject_grades[subject_name] = f"{grade_secured}"
                    subject_grades[f"{subject_name} Grade Point"] = grade_points
                elif sub_code.endswith(('J', 'N', 'O', 'F', 'B', 'I')) and sub_code[:-1].isdigit() and 500 <= int(sub_code[:-1]) < 600:
                    subject_name = cells[1].text.strip()
                    if len(cells) > 4:
                        grade_secured = cells[4].text.strip()
                    elif len(cells) > 3:
                        grade_secured = cells[3].text.strip()
                    else:
                        grade_secured = 'N/A'
                    grade_points = grade_to_points.get(grade_secured, 'N/A')
                    # Add the grade secured and grade points to the subject_grades dictionary
                    subject_grades[subject_name] = f"{grade_secured}"
                    subject_grades[f"{subject_name} Grade Point"] = grade_points
        details.update(subject_grades)
    else:
        print("Marks Table not found")

    return details


# Main code to process roll numbers and store results in Excel
roll_numbers_1 = range(245621733001, 245621733196)
roll_numbers_2 = range(245621733301, 245621733320)

roll_numbers = list(roll_numbers_1) + list(roll_numbers_2)

results = []

session = requests.Session()
session.get(url)

for roll_number in roll_numbers:
    html_content = get_result_page(roll_number, session)
    if html_content:
        details = extract_details(html_content)
        if 'SGPA' in details:
            sgpa_value = details['SGPA']
            if sgpa_value == 'Promoted':
                result = {'Roll No': roll_number, 'SGPA': sgpa_value}
            else:
                result = {'Roll No': roll_number, 'SGPA': float(sgpa_value)}
            result.update(details)
            results.append(result)
            print(f"Processed Roll No: {roll_number}")
        else:
            print(f"SGPA not found or not relevant for Roll No: {roll_number}")
    else:
        print(f"Failed to retrieve results for Roll No: {roll_number}")

# Store results in Excel
df = pd.DataFrame(results)
df.to_excel('students_5.xlsx', index=False)
