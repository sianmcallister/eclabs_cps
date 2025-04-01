import os
import re
import csv
import PyPDF2

def extract_text_from_pdf(file_path, max_pages=50):
    """Extract text from a PDF file up to a given number of pages."""
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = min(max_pages, len(reader.pages))
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text() or ""
    return text

def clean_pi_organization(text):
    """Extract only the school name from PI Organization field."""
    match = re.search(r"PI Organization\s*([\w\W]+?)If the form indicates", text, re.DOTALL)
    return match.group(1).strip() if match else "Not Found"

def extract_information(text):
    """Extract only required fields using regex patterns."""
    patterns = {
        "RRB Number": r"RRB Number\s*(\S+)",
        "Study Title": r"Study Title\s*([\w\W]+?)Event Type",
        "PI Organization": clean_pi_organization(text),
        "Primary Funding Source": r"Who is the primary funding source\?\s*([\w\W]+?)What is the amount",
        "Amount of Funding Awarded": r"What is the amount of funding awarded\?\s*\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)"
    }
    
    extracted_info = {}
    for key, pattern in patterns.items():
        if key == "PI Organization":
            extracted_info[key] = pattern
        else:
            match = re.search(pattern, text, re.DOTALL)
            extracted_info[key] = match.group(1).strip() if match else "Not Found"
    
    return extracted_info

def process_pdfs(pdf_folder, output_csv):
    """Process all PDFs in a folder and save extracted data to CSV."""
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        headers = ["RRB Number", "Study Title", "PI Organization", "Primary Funding Source", "Amount of Funding Awarded"]
        writer.writerow(headers)
        
        for filename in os.listdir(pdf_folder):
            if filename.endswith(".pdf"):
                file_path = os.path.join(pdf_folder, filename)
                text = extract_text_from_pdf(file_path)
                extracted_info = extract_information(text)
                writer.writerow([extracted_info.get(header, "Not Found") for header in headers])

if __name__ == "__main__":
    pdf_folder = "/Users/muthukumarsundar/Documents/GitHub/eclabs_cps/pdfs/CPS RRB Application Files (PDF)"  # Folder containing PDFs
    output_csv = "smaller_rrb_extracted_data.csv"  # Output CSV file
    process_pdfs(pdf_folder, output_csv)
