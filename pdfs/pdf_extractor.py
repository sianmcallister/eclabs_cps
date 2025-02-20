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

def extract_information(text):
    """Extract required information using regex patterns."""
    patterns = {
        "RRB Number": r"RRB Number\s*(\S+)",
        "Study Title": r"Study Title\s*([\w\W]+?)Event Type",
        "Submitter": r"Submitter\s*([\w\W]+?)Email:",
        "Email": r"Email:\s*(\S+)",
        "PI Organization": r"PI Organization\s*([\w\W]+?)Is the Principal Investigator",
        "Primary Funding Source": r"Who is the primary funding source\?\s*([\w\W]+?)What is the amount",
        "Amount of Funding Awarded": r"What is the amount of funding awarded\?\s*\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",
        "Potential School Sites": r"Please select all potential school sites involved with this study\s*([\w\W]+?)Will this research",
        "Outline of Protocol": r"Please outline your protocol for individual interview activities,\s*([\w\W]+?)Does this involve video",
        "Executive Summary": r"Executive Summary or Abstract\s*([\w\W]+?)Research Questions",
        "Research Questions": r"Research Questions and Hypothesis\s*([\w\W]+?)Purpose",
        "Purpose": r"Purpose and Literature Review\s*([\w\W]+?)Research Activities",
        "Research Activities": r"Research Activities\s*([\w\W]+?)Research Methodology",
        "Research Methodology": r"Research Methodology\s*([\w\W]+?)Benefits"
    }
    
    extracted_info = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        extracted_info[key] = match.group(1).strip() if match else "Not Found"
    
    return extracted_info

def process_pdfs(pdf_folder, output_csv):
    """Process all PDFs in a folder and save extracted data to CSV."""
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        headers = [
            "RRB Number", "Study Title", "Submitter", "Email", "PI Organization",
            "Primary Funding Source", "Amount of Funding Awarded", "Potential School Sites",
            "Outline of Protocol", "Executive Summary", "Research Questions", "Purpose",
            "Research Activities", "Research Methodology"
        ]
        writer.writerow(headers)
        
        for filename in os.listdir(pdf_folder):
            if filename.endswith(".pdf"):
                file_path = os.path.join(pdf_folder, filename)
                text = extract_text_from_pdf(file_path)
                extracted_info = extract_information(text)
                writer.writerow([extracted_info.get(header, "Not Found") for header in headers])

if __name__ == "__main__":
    pdf_folder = "CPS RRB Application Files (PDF) "  # Folder containing PDFs
    output_csv = "rrb_extracted_data.csv"  # Output CSV file
    process_pdfs(pdf_folder, output_csv)