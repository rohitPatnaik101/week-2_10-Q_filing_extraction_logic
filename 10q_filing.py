import pdfplumber
import re

def extract_company_name(text):
    match = re.search(r"(.*?)\n(?=\(?Exact name of registrant as specified in its charter\)?)", text, re.IGNORECASE)
    return match.group(1).strip() if match else None

def extract_filing_date(text):
    match = re.search(r"For the quarterly period ended\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})", text)
    return match.group(1).strip() if match else None

def find_item_2_page(text):
    match = re.search(r"Item\s+2\.\s+Management’s Discussion and Analysis.*?(\d{1,3})", text, re.IGNORECASE)
    return int(match.group(1)) if match else None

def extract_item_2_paragraphs(pdf, page_number, num_paragraphs=2):
    if page_number is None or page_number >= len(pdf.pages):
        return None

    page = pdf.pages[page_number - 1]  # pdfplumber uses 0-based index
    text = page.extract_text()
    if not text:
        return None

    paragraphs = text.split("\n\n")  # Assuming paragraphs are separated by double newlines
    return "\n\n".join(paragraphs[:num_paragraphs]).strip() if paragraphs else None

def extract_10q_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

        company_name = extract_company_name(full_text)
        filing_date = extract_filing_date(full_text)
        item_2_page = find_item_2_page(full_text)

        item_2_text = extract_item_2_paragraphs(pdf, item_2_page)

        return {
            "Company Name": company_name,
            "Filing Date": filing_date,
            "Item 2 Excerpt": item_2_text
        }

if __name__ == "__main__":
    pdf_filename = "SandPGlobal-1Q-2024-10-Q.pdf"
    extracted_data = extract_10q_data(pdf_filename)

    print("Company Name:", extracted_data["Company Name"])
    print("Filing Date:", extracted_data["Filing Date"])
    print("\nItem 2 Excerpt:")
    print(extracted_data["Item 2 Excerpt"])
