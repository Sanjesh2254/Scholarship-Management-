# Copyright (c) 2025, sanjesh and contributors
# For license information, please see license.txt

from frappe.model.document import Document
import frappe
import pytesseract
from PIL import Image
import os
import os
import re
import frappe
from PIL import Image
import pytesseract
from frappe.utils import today


class ScholarshipRenewal(Document):

    def after_insert(self):
        self.status="Applied"
        self.renewal_date=today()
        doc = frappe.get_doc("Scholarship Application", self.scholarship_name)
        fieldname = "previous_semester_marksheet"  
        fieldname1="income_certificate"
        if doc.previous_semester_marksheet:

            file_url = doc.get(fieldname)
            if not file_url:
                frappe.throw(f"No file attached in field: {fieldname}")

            # Correct file path
            file_path = frappe.get_site_path("public", file_url.lstrip("/"))

            if not os.path.exists(file_path):
                frappe.throw(f"File not found: {file_path}")

            # Open the image using PIL (Python Imaging Library)
            img = Image.open(file_path)

            # Convert webp → png if needed
            if file_path.lower().endswith(".webp"):
                temp_path = file_path.replace(".webp", ".png")
                img.save(temp_path)
                img = Image.open(temp_path)

            text = pytesseract.image_to_string(img)

            total_marks = None
            match_total_marks = re.search(r"Total\s*[:\s]*([0-9]+)", text, re.IGNORECASE)

            if match_total_marks:
                total_marks = match_total_marks.group(1)
            if self.scholarship_name == doc.name:
                if doc.previous_semester_marksheet:
                    if int(applicant.cgpa) < int(total_marks):
                        frappe.throw("You are not eligible for this Renewal Scholarship.")


        file_url = doc.get(fieldname1)
        if not file_url:
            frappe.throw(f"No file attached in field: {fieldname1}")


        file_path = frappe.get_site_path("public", file_url.lstrip("/"))

        if not os.path.exists(file_path):
            frappe.throw(f"File not found: {file_path}")

        img = Image.open(file_path)

        if file_path.lower().endswith(".webp"):
            temp_path = file_path.replace(".webp", ".png")
            img.save(temp_path)
            img = Image.open(temp_path)

        text = pytesseract.image_to_string(img)
        income = None
        match_income = re.search(r"Income\s*[:\s]*([0-9,]+)", text, re.IGNORECASE)
        if match_income:
            income = match_income.group(1)
            income = re.sub(r"[^\d]", "", income)
        applicant = frappe.get_doc("Applicant Profile", self.applicant)
        if self.scholarship_name == doc.name:
            if doc.income_certificate:
                applicant = frappe.get_doc("Applicant Profile", self.applicant)

                if int(applicant.income) < int(income):
                    print(int(applicant.income))
                    print(income)
                    frappe.throw("Please update your Income Certificate.")

        else:
            frappe.throw("The Scholarship Renewal record does not match the Scholarship Application.")
        try:
            send_email_renewal=frappe.db.get_single_value("Scholarship Settings","send_email_renewal")
            if send_email_renewal == 1:
                user = frappe.session.user
                recipient_email = frappe.db.get_value("Applicant Profile", self.applicant, "email")
                applicant_full_name = frappe.db.get_value("User", user, "full_name")

                pdf = frappe.get_print(
                    doc=self,
                    print_format="Scholarship Renewal",  
                    doctype="Scholarship Renewal",
                    as_pdf=True
                )

                frappe.sendmail(
                    recipients=[recipient_email],
                    subject=f"Scholarship Renewal Submitted - {self.name}",
                    message=f"""
                        <div style="font-family: Arial, sans-serif; color: #333; padding: 20px; background-color: #f4f6f8;">
                            <div style="text-align: center; padding: 20px 0; border-bottom: 3px solid #4CAF50; background-color: #ffffff; border-radius: 6px 6px 0 0;">
                                <img src="https://media.istockphoto.com/id/1366851749/vector/scholarship-banner.jpg?s=612x612&w=0&k=20&c=qFKJiZGmD97vYxqi0qiTolbHV3fDgjYuhNtTbj7cndM=" 
                                    alt="Scholarship Logo" 
                                    style="max-height: 120px; margin-bottom: 10px;">
                                <h2 style="color: #4CAF50; margin: 0; font-size: 26px;">Scholarship Renewal Confirmation</h2>
                            </div>

                            <div style="background-color: #ffffff; padding: 20px; border-radius: 0 0 6px 6px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                                <p style="font-size: 16px;">Hello <strong>{applicant_full_name}</strong>,</p>
                                <p style="font-size: 15px; line-height: 1.6;">
                                    We are pleased to inform you that your scholarship  renewal has been successfully submitted.
                                </p>

                                <table style="border-collapse: collapse; width: 100%; margin-top: 15px; font-size: 14px;">
                                    <tr>
                                        <td style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;"><strong> Renewal Application ID</strong></td>
                                        <td style="padding: 10px; border: 1px solid #ddd;">{self.name}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;"><strong>Scholarship Name</strong></td>
                                        <td style="padding: 10px; border: 1px solid #ddd;">{self.scholarship_name}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;"><strong>Status</strong></td>
                                        <td style="padding: 10px; border: 1px solid #ddd;">Applied</td>
                                    </tr>
                                </table>

                                <p style="margin-top: 20px; font-size: 15px; line-height: 1.6;">
                                    We will review your Scholarship Renewal Application and notify you of the next steps soon.
                                </p>

                                <p style="color: #777; font-size: 12px; margin-top: 20px;">
                                    Regards,<br>
                                    <strong>Scholarship Management Team</strong>
                                </p>
                            </div>
                        </div>
                    """,
                    attachments=[{
                        "fname": f"{self.name}.pdf",
                        "fcontent": pdf
                    }],
                    now=True
                )

                frappe.msgprint(f"Confirmation email with PDF sent to {recipient_email}")

        except Exception:
            frappe.log_error(frappe.get_traceback(), "Scholarship Email Error")
            frappe.msgprint("Failed to send confirmation email. Please check email settings.")

        
    def on_submit(self):
        self.payment_credited=today()


        
@frappe.whitelist()
def auto_fill(scholarship_name=None):
    user_email = frappe.db.get_value("User", frappe.session.user, "email")
    if not user_email:
        return {}

    applicant_name = frappe.db.get_value("Applicant Profile", {"email": user_email}, "name")
    if not applicant_name:
        return {}

    applicant = frappe.get_doc("Applicant Profile", applicant_name)

    result = {
        "applicant": applicant.name,
        "passbook":applicant.passbook,
        "tamil_medium_certificate":applicant.tamil_medium_certificate
    }

    if scholarship_name:
        scholarship = frappe.get_doc("Scholarship Application", scholarship_name)

        if scholarship.previous_semester_marksheet:
            result["previous_semester_marksheet"] = applicant.previous_semester_marksheet

        if scholarship.income_certificate:
            result["income_certificate"] = applicant.income_certificate

        if scholarship.tenth_marksheet:
            print(applicant.tenth_marksheet)
            result["tenth_marksheet"] = applicant.tenth_marksheet

        if scholarship.eleventh_marksheet:
            result["eleventh_marksheet"] = applicant.eleventh_marksheet

        if scholarship.twelfth_marksheet:
            result["twelfth_marksheet"] = applicant.twelfth_marksheet

        if scholarship.community_certificate:
            result["community_certificate"] = applicant.community_certificate
        

    return result


@frappe.whitelist()
def get_permission_query_conditions(user):
    roles = frappe.get_roles(user)

    if "System Manager" in roles or "Scholarship Committee" in roles or "Finance Department" in roles or "Document Verifier" in roles:
        return None 
    # user_email = frappe.db.get_value("User", user, "email")
    # if not user_email:
    #     return "1=0"  

    # applicant_name = frappe.db.get_value("Applicant Profile", {"email": user_email}, "name")
    # if not applicant_name:
    #     return "1=0"   
    # return f"`tabScholarship Renewal`.`applicant` = '{applicant_name}'"

@frappe.whitelist()
def check_existing_application(scholarship_name, applicant):
    existing_application=frappe.db.exists(
        "Scholarship Renewal",
        {
            "scholarship_name": scholarship_name,
            "applicant": applicant,
            "docstatus": ["<", 2] 
        }
    )
    print(existing_application)
    return bool(existing_application)


    


@frappe.whitelist()
def get_allowed_scholarships():
    return frappe.db.get_list(
        "Setting test",
        filters={"parent": "Scholarship Settings"},
        pluck="test"
    )

