# Copyright (c) 2025, sanjesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import re

class IncomeCertificate(Document):
	pass
import frappe
import pytesseract
from PIL import Image
import re

@frappe.whitelist()
def extract_income_certificate(docname):
    # Get the Income Certificate document
    doc = frappe.get_doc("Income Certificate", docname)

    if not doc.certificate:
        frappe.throw("Please upload the income certificate.")

    # Get file path from the File doctype
    file_doc = frappe.get_doc("File", {"file_url": doc.certificate})
    file_path = file_doc.get_full_path()

    # OCR: Read image
    text = pytesseract.image_to_string(Image.open(file_path))

    # Extract Name
    name_match = re.search(r"Name\s+([A-Za-z ]+)", text, re.IGNORECASE)
    extracted_name = name_match.group(1).strip() if name_match else ""

    # Extract Income
    income_match = re.search(r"Income\s+([\d,]+)", text, re.IGNORECASE)
    extracted_income = income_match.group(1).strip() if income_match else ""

    # Save values to the document
    doc.extracted_name = extracted_name
    doc.extracted_income = extracted_income
    doc.save(ignore_permissions=True)

    return {"name": extracted_name, "income": extracted_income}
