# Copyright (c) 2025, sanjesh and contributors
import frappe
from frappe.model.document import Document
from frappe.utils import today

class Transaction(Document):
    def before_save(self):
        self.transaction_date = today()

    def after_insert(self):
        send_email_approval = frappe.db.get_single_value("Scholarship Settings", "send_email_approval")

        if send_email_approval == 1:
            user = frappe.session.user
            recipient_email = frappe.db.get_value("Applicant Profile", self.applicant, "email")
            applicant_full_name = frappe.db.get_value("User", user, "full_name")

            pdf = frappe.get_print(
                "Transaction",          # Doctype
                self.name,              # Doc name
                print_format="Transaction",
                as_pdf=True
            )

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
                        <p style="font-size: 16px;">Hello,</p>
                        <p style="font-size: 15px; line-height: 1.6;">
                            We are pleased to inform you that your scholarship application has been successfully Approved. Congratulations!
                        </p>

                        <!-- Application Details Table -->
                        <table style="border-collapse: collapse; width: 100%; margin-top: 15px; font-size: 14px;">
                            <tr>
                                <td style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;"><strong>Application ID</strong></td>
                                <td style="padding: 10px; border: 1px solid #ddd;">{self.applicant}</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;"><strong>Scholarship Name</strong></td>
                                <td style="padding: 10px; border: 1px solid #ddd;">{self.scholarship}</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;"><strong>Status</strong></td>
                                <td style="padding: 10px; border: 1px solid #ddd;">{self.transaction_type}</td>
                            </tr>
                        </table>

                        <p style="margin-top: 20px; font-size: 15px; line-height: 1.6;">
                            The future belongs to those who believe in the beauty of their dreams.
                        </p>
                        Please fill the feedback using the link below:

                            <a href="http://127.0.0.1:8007/feedback">Click here to feedback</a>
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

            frappe.msgprint(f"Confirmation email sent to {recipient_email}")
