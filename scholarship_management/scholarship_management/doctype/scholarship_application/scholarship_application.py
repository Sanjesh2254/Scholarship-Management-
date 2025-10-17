# Copyright (c) 2025, sanjesh and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate, add_months
from frappe.model.document import Document
from frappe.utils import today
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
class ScholarshipApplication(Document):
    def autoname(self):
        scholarship_name = self.scholarship_name
        applicant = self.applicant
        self.name = make_autoname(scholarship_name+"-"+applicant+"-"+".####")

    def before_save(self):
        print("save")
        previous_status = self.get_db_value("status")
        if previous_status and previous_status != self.status:
            print(previous_status)
            print(self.status)
            send_status_notification(self)
        # self.applicant = applicant
        print(self.tenth_marksheet)
        self.application_date=today()
        scholarship_name= self.scholarship_name
        max_applicants = frappe.db.count('Scholarship Application', {'scholarship_name': scholarship_name})
        max_applicants_allowed = frappe.get_value('Scholarship', scholarship_name, 'max_applicants_allowed')
        if max_applicants >= max_applicants_allowed:
            doc = frappe.get_doc('Scholarship', scholarship_name)
            doc.status = 'Closed'
            doc.save()
            frappe.db.commit()
        if max_applicants > max_applicants_allowed:
            frappe.throw("Application limit reached. This scholarship is now closed.")
        
    def after_insert(self):
        try:
            self.status="Applied"
            send_email_approval=frappe.db.get_single_value("Scholarship Settings","send_email_approval")
            if send_email_approval == 1:
                user = frappe.session.user
                recipient_email = frappe.db.get_value("Applicant Profile", self.applicant, "email")
                applicant_full_name = frappe.db.get_value("User", user, "full_name")

                pdf = frappe.get_print(
                    doc=self,
                    print_format="Scholarship Application",  
                    doctype="Scholarship Application",
                    as_pdf=True,
                    docname=self.name,
                    no_Letterhead=0,
                    Letterhead=None,
                    orientation="portrait",
                    format_options=None,
                    lang=None,
                    print_Letter = 0
                )

                frappe.sendmail(
                    recipients=[recipient_email],
                    subject=f"Scholarship Application Submitted - {self.name}",
                    message=f"""
                        <div style="font-family: Arial, sans-serif; color: #333; padding: 20px; background-color: #f4f6f8;">
                            <div style="text-align: center; padding: 20px 0; border-bottom: 3px solid #4CAF50; background-color: #ffffff; border-radius: 6px 6px 0 0;">
                                <img src="https://media.istockphoto.com/id/1366851749/vector/scholarship-banner.jpg?s=612x612&w=0&k=20&c=qFKJiZGmD97vYxqi0qiTolbHV3fDgjYuhNtTbj7cndM=" 
                                    alt="Scholarship Logo" 
                                    style="max-height: 120px; margin-bottom: 10px;">
                                <h2 style="color: #4CAF50; margin: 0; font-size: 26px;">Scholarship Application Confirmation</h2>
                            </div>

                            <div style="background-color: #ffffff; padding: 20px; border-radius: 0 0 6px 6px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                                <p style="font-size: 16px;">Hello <strong>{applicant_full_name}</strong>,</p>
                                <p style="font-size: 15px; line-height: 1.6;">
                                    We are pleased to inform you that your scholarship application has been successfully submitted.
                                </p>

                                <table style="border-collapse: collapse; width: 100%; margin-top: 15px; font-size: 14px;">
                                    <tr>
                                        <td style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;"><strong>Application ID</strong></td>
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
                                    We will review your application and notify you of the next steps soon.
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
        self.payment_credited = today()


def send_status_notification(doc):
    try:
        user = frappe.db.get_value("Applicant Profile", doc.applicant, "email")  
        # user="sanjeshtridots@gmail.com"
        if not user:
            frappe.log_error(f"No linked system user found for applicant {doc.applicant}", "Scholarship Notification")
            return

        message = f"Your scholarship application {doc.scholarship_name} status has been updated to: {doc.status}"

        frappe.publish_realtime(
            event="scholarship_status_notification",
            message=message,
            user=user
        )

        frappe.get_doc({
            "doctype": "Notification Log",
            "subject": f"Scholarship Application Status Update - {doc.name}",
            "document_type": "Scholarship Application",
            "document_name": doc.name,
            "from_user": frappe.session.user,
            "for_user": user,
            "email_content": message
        }).insert(ignore_permissions=True)

    except Exception:
        frappe.log_error(frappe.get_traceback(), "Scholarship Status Notification Error")



@frappe.whitelist()
def check_existing_application(scholarship_name, applicant):
    existing_application=frappe.db.exists(
        "Scholarship Application",
        {
            "scholarship_name": scholarship_name,
            "applicant": applicant,
            "docstatus": ["<", 2] 
        }
    )
    return bool(existing_application)

def get_permission_query_conditions(user):
    roles = frappe.get_roles(user)
    if "System Manager" in roles or "Scholarship Committee" in roles or "Finance Department" in roles or "Document Verifier" in roles:
        return None  


def fatch_applicant():
    user_email = frappe.db.get_value("User", frappe.session.user, "email")
    applicant = frappe.db.get_value("Applicant Profile", {"email": user_email})
    self.community_certificate = applicant.community_certificate
    self.income_certificate = applicant.income_certificate


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
        scholarship = frappe.get_doc("Scholarship", scholarship_name)


        if getattr(scholarship, "cgpa", 0) > 0:
            result["previous_semester_marksheet"] = applicant.previous_semester_marksheet

        if getattr(scholarship, "income", 0) > 0:
            result["income_certificate"] = applicant.income_certificate

        if getattr(scholarship, "tenth_mark", 0) > 0:
            print(applicant.tenth_marksheet)
            result["tenth_marksheet"] = applicant.tenth_marksheet

        if getattr(scholarship, "eleventh_mark", 0) > 0:
            result["eleventh_marksheet"] = applicant.eleventh_marksheet

        if getattr(scholarship, "twelfth_mark", 0) > 0:
            result["twelfth_marksheet"] = applicant.twelfth_marksheet
        
        if scholarship.caste and len(scholarship.caste) > 0: 
            result["community_certificate"] = applicant.community_certificate

    return result


from frappe.utils import today, add_days

@frappe.whitelist()
def create_future_scholarships():
    date = today()
    start_date = date
    end_date = add_days(date, 30)
    scholarship_name = f"Scholarship {frappe.utils.formatdate(date, 'MMMM yyyy')}"

    if not frappe.db.exists("Scholarship", {"name": scholarship_name}):
        scholarship = frappe.get_doc({
            "doctype": "Scholarship",
            "name": scholarship_name,  
            "name1": scholarship_name,
            "total_amount": 25000,
            "start_date": start_date,
            "end_date": end_date,
            "max_applicants_allowed": 10,
            "status": "Active"
        })
        scholarship.insert()
        frappe.db.commit()
        frappe.msgprint(f"Created: {scholarship_name}")
    else:
        frappe.msgprint(f"Already exists: {scholarship_name}")
