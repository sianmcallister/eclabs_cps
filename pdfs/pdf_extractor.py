import os
import re
import csv
import PyPDF2

# Function to extract text up to page 50
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = min(50, len(reader.pages))  # Limit to 50 pages
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Function to extract key information using regex
def extract_information(text):
    info = {
        "RRB Number": re.search(r"RRB Number\s*(\S+)", text),
        "Study Title": re.search(r"Study Title\s*([\w\W]+?)Event Type", text),
        "Schools Participating": re.search(r"Schools Participating\s*([\w\W]+?)Submitter", text),
        "Submitter": re.search(r"Submitter\s*([\w\W]+?)Email:", text),
        "Email": re.search(r"Email:\s*(\S+)", text),
        "Business Phone": re.search(r"Business Phone:\s*(\S+)", text),
        "RRP Affiliation": re.search(r"RPP with which you are affiliated\s*([\w\W]+?)RPP Point of Contact", text),
        "RRP Point of Contact": re.search(r"RPP Point of Contact\s*([\w\W]+?)Email", text),
        "PI Organization": re.search(r"PI Organization\s*([\w\W]+?)Is the Principal Investigator", text),
        "Student or CPS Staff": re.search(r"Is the Principal Investigator a Student\?\s*(\w+)", text),
        "Primary Funding Source": re.search(r"primary funding source\?\s*([\w\W]+?)What is the amount", text),
        "Amount of Funding Awarded": re.search(r"Amount of Funding Awarded\s*\$([\d,\.]+)", text),
        "Potential School Sites": re.search(r"potential school sites involved\s*([\w\W]+?)Will this research", text),
        "Outline of Protocol": re.search(r"outline your protocol for focus group activities,\s*([\w\W]+?)Student focus groups", text),
        "Executive Summary": re.search(r"Executive Summary or Abstract\s*([\w\W]+?)Research Questions", text),
        "Research Questions": re.search(r"Research Questions and Hypothesis\s*([\w\W]+?)Purpose and Literature Review", text),
        "Purpose and Literature Review": re.search(r"Purpose and Literature Review\s*([\w\W]+?)Research Activities", text),
        "Research Activities": re.search(r"Research Activities\s*([\w\W]+?)Research Methodology", text),
        "Research Methodology": re.search(r"Research Methodology\s*([\w\W]+?)Benefits and Commitment", text)
    }
    # Extract found groups or default to "Not Found"
    extracted_info = {key: (match.group(1).strip() if match else "Not Found") for key, match in info.items()}
    return extracted_info

# Main function to iterate through PDFs and save to CSV
def main(pdf_folder, output_csv):
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["RRB Number", "Study Title", "Schools Participating", "Submitter", "Email", "Business Phone", "RRP Affiliation", "RRP Point of Contact", "PI Organization", "Student or CPS Staff", "Primary Funding Source", "Amount of Funding Awarded", "Potential School Sites", "Outline of Protocol", "Executive Summary", "Research Questions", "Purpose and Literature Review", "Research Activities", "Research Methodology"])

        for filename in os.listdir(pdf_folder):
            if filename.endswith(".pdf"):
                file_path = os.path.join(pdf_folder, filename)
                text = extract_text_from_pdf(file_path)
                extracted_info = extract_information(text)
                writer.writerow(extracted_info.values())

if __name__ == "__main__":
    pdf_folder = "CPS RRB Application Files (PDF) "  # Folder containing PDFs
    output_csv = "output.csv"  # Output CSV file
    main(pdf_folder, output_csv)