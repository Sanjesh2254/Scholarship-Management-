# Copyright (c) 2025, sanjesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today
import frappe
from frappe.model.document import Document

class ScholarshipApplication(Document):
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
        # self.status='Applied'
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
            user = frappe.session.user
            recipient_email = frappe.db.get_value("Applicant Profile", self.applicant, "email")
            applicant_full_name = frappe.db.get_value("User", user, "full_name")

            pdf = frappe.get_print(
                doc=self,
                print_format="Scholarship Application",  
                doctype="Scholarship Application",
                as_pdf=True
            )

            # Send email with PDF attachment
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
        self.payment_credited=today()
        send_email_approval=frappe.db.get_single_value("Scholarship Settings","send_email_approval")
        if send_email_approval == 1:
          
            user = frappe.session.user
            recipient_email = frappe.db.get_value("Applicant Profile", self.applicant, "email")
            applicant_full_name = frappe.db.get_value("User", user, "full_name")
            frappe.sendmail(
                recipients=[recipient_email],
                subject=f"Scholarship Application Submitted - {self.name}",
                message=f"""
                <div style="font-family: Arial, sans-serif; color: #333; padding: 20px; background-color: #f4f6f8;">
    
    <!-- Header with larger logo -->
    <div style="text-align: center; padding: 20px 0; border-bottom: 3px solid #4CAF50; background-color: #ffffff; border-radius: 6px 6px 0 0;">
        <img src="https://media.istockphoto.com/id/1366851749/vector/scholarship-banner.jpg?s=612x612&w=0&k=20&c=qFKJiZGmD97vYxqi0qiTolbHV3fDgjYuhNtTbj7cndM=" 
            alt="Scholarship Logo" 
            style="max-height: 120px; margin-bottom: 10px;">
        <h2 style="color: #4CAF50; margin: 0; font-size: 26px;">Scholarship Approved Confirmation</h2>
    </div>

    <!-- Body content -->
    <div style="background-color: #ffffff; padding: 20px; border-radius: 0 0 6px 6px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
        <p style="font-size: 16px;">Hello <strong>{applicant_full_name}</strong>,</p>
        <p style="font-size: 15px; line-height: 1.6;">
            We are pleased to inform you that your scholarship application has been successfully Approved Congratulations!.         </p>

        <!-- Application Details Table -->
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
                <td style="padding: 10px; border: 1px solid #ddd;">{self.status}</td>
            </tr>
        </table>

        <p style="margin-top: 20px; font-size: 15px; line-height: 1.6;">
        The future belongs to those who believe in the beauty of their dreams.
        </p>

        <p style="color: #777; font-size: 12px; margin-top: 20px;">
            Regards,<br>
            <strong>Scholarship Management Team</strong>
        </p>
    </div>
</div>
                """,
                now=True
            )

            frappe.msgprint(f"Confirmation email sent to {recipient_email}")

     

# This function is outside the class
def send_status_notification(doc):
    try:
        # Try fetching the linked system user
        # user = frappe.db.get_value("Applicant Profile", doc.applicant, "email")  # change to your field
        user="sanjeshtridots@gmail.com"
        if not user:
            frappe.log_error(f"No linked system user found for applicant {doc.applicant}", "Scholarship Notification")
            return

        message = f"Your scholarship application {doc.scholarship_name} status has been updated to: {doc.status}"

        # Realtime popup
        frappe.publish_realtime(
            event="scholarship_status_notification",
            message=message,
            user=user
        )

        # Add to Notification Center
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
    if "System Manager" in frappe.get_roles(user):
        return None 
    user_email = frappe.db.get_value("User", user, "email")
    if not user_email:
        return "1=0"  

    applicant_name = frappe.db.get_value("Applicant Profile", {"email": user_email}, "name")
    if not applicant_name:
        return "1=0"   
    return f"`tabScholarship Application`.`applicant` = '{applicant_name}'"

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



# setting=frapppe.db.get_single_value("Scholarship Setting","caste_allocate")
# caste=setting.caste_name
# percentage=setting.percentage

# scholarship=frappe.get_doc("Scholarship Application")
