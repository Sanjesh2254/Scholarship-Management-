# Copyright (c) 2025, sanjesh and contributors
# For license information, please see license.txt

import frappe
import re
import os
import re
import frappe
import pytesseract
from PIL import Image
from frappe.model.document import Document
from frappe.utils import today
from dateutil.relativedelta import relativedelta
from datetime import date




class ApplicantProfile(Document):
    def is_valid_aadhar(self):
        aadhar = self.aadhaar_number  
        return bool(re.fullmatch(r"^[2-9]{1}[0-9]{11}$", str(aadhar)))

    def before_save(self):
        user_email = frappe.db.get_value("User", frappe.session.user, "email")
        self.email = user_email
        self.update_date=today()

        if self.dob:
            self.age = relativedelta(date.today(), frappe.utils.getdate(self.dob)).years

        if self.aadhaar_number and not self.is_valid_aadhar():
            frappe.throw("Invalid Aadhaar number")


@frappe.whitelist()
def get_permission_query_conditions(user):
    roles = frappe.get_roles(user)
    if "System Manager" in roles or "Scholarship Committee" in roles or "Finance Department" in roles or "Document Verifier" in roles:
        return None

    # user_email = frappe.db.get_value("User", user, "email")
    # if not user_email:
    #     return "1=0"
    # return f"`tabApplicant Profile`.`email` = '{user_email}'"


@frappe.whitelist()
def ocr_text(docname, fieldname):
    doc = frappe.get_doc("Applicant Profile", docname)

    file_url = doc.get(fieldname)
    if not file_url:
        frappe.throw(f"No file attached in field: {fieldname}")

    try:
        file_path = frappe.get_site_path("public", file_url.lstrip("/"))

        if not os.path.exists(file_path):
            frappe.throw(f"File not found: {file_path}")

        img = Image.open(file_path)

        # Convert webp → png if needed
        if file_path.lower().endswith(".webp"):
            temp_path = file_path.replace(".webp", ".png")
            img.save(temp_path)
            img = Image.open(temp_path)

        # OCR extraction
        text = pytesseract.image_to_string(img)
        income = None
        match_income = re.search(r"Income\s*[:\s]*([0-9,]+)", text, re.IGNORECASE)
        if match_income:
            income = match_income.group(1)
            income = re.sub(r"[^\d]", "", income)

        if income:
            field_map_income = {
                "income_certificate": "income"
            }
            if fieldname in field_map_income:
                doc.db_set(field_map_income[fieldname], income)
        
            return {
                "ocr_text": {"income": income}
            }


        caste_info = None
        match_caste = re.search(r"belongs to\s*[:\s]*([A-Za-z]+)", text, re.IGNORECASE)
        if match_caste:
            caste_info = match_caste.group(1)

        if caste_info:
            field_map_caste = {
                "community_certificate": "caste"
            }
            if fieldname in field_map_caste:
                doc.db_set(field_map_caste[fieldname], caste_info)
            
            return {
                "ocr_text": {"caste": caste_info}
            }

        total_marks = None
        match_total_marks = re.search(r"Total\s*[:\s]*([0-9]+)", text, re.IGNORECASE)
        if match_total_marks:
            total_marks = match_total_marks.group(1)

        if not total_marks:
            frappe.throw("Could not find Total Marks in the uploaded document.")

        field_map_total_marks = {
            "previous_semester_marksheet": "previous_semester_total",
            "tenthmarksheet": "tenth_total",
            "eleventhmarksheet": "eleventh_total",
            "twelfthmarksheet": "twelfth_total",
            "tenth_marksheet": "tenth_mark",
            "eleventh_marksheet": "eleventh_mark",
            "twelfth_marksheet": "twelfth_mark"
        }

        if fieldname in field_map_total_marks:
            doc.db_set(field_map_total_marks[fieldname], total_marks)

    
        return {
            "ocr_text": {"total_marks": total_marks}
        }

    except Exception as e:
        frappe.log_error(f"OCR Failed: {e}", "OCR Error")
        frappe.throw("OCR failed. Check the error logs.")
