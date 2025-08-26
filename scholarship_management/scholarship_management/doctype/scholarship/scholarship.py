import frappe
import re
from frappe.model.document import Document
from frappe.utils import getdate

class Scholarship(Document):
    def after_insert(self):
        # Get all system users (exclude Guest / Administrator if you want)
        users = frappe.get_all("User", filters={"enabled": 1}, pluck="email")

        # Remove Administrator and Guest
        users = [u for u in users if u not in ["Administrator", "Guest"]]

        if users:
            subject = f"🎓 New Scholarship Created: {self.name1}"
            message = f"""
            <div style="font-family: Arial, sans-serif; max-width:600px; margin:20px auto; 
            border:1px solid #e0e0e0; border-radius:6px; background:#ffffff;">

    <!-- Header with Logo -->
    <div style="text-align: center; padding: 20px 0; border-bottom: 3px solid #4CAF50; 
                background-color: #ffffff; border-radius: 6px 6px 0 0;">
        <img src="https://media.istockphoto.com/id/1366851749/vector/scholarship-banner.jpg?s=612x612&w=0&k=20&c=qFKJiZGmD97vYxqi0qiTolbHV3fDgjYuhNtTbj7cndM=" 
             alt="Scholarship Logo" 
             style="max-height: 120px; margin-bottom: 10px;">
        <h2 style="color: #4CAF50; margin: 0; font-size: 26px;">🎓 New Scholarship Available!</h2>
    </div>

    <!-- Body -->
    <div style="padding:20px;">
        <p style="font-size:15px; color:#333;">
            Hello,<br><br>
            A new scholarship has been created. Please find the details below:
        </p>
        
        <table style="width:100%; border-collapse:collapse; margin:15px 0;">
            <tr>
                <td style="padding:8px; font-weight:bold; border-bottom:1px solid #ddd;">Scholarship Name</td>
                <td style="padding:8px; border-bottom:1px solid #ddd;">{self.name1}</td>
            </tr>
            <tr>
                <td style="padding:8px; font-weight:bold; border-bottom:1px solid #ddd;">Start Date</td>
                <td style="padding:8px; border-bottom:1px solid #ddd;">{self.start_date}</td>
            </tr>
            <tr>
                <td style="padding:8px; font-weight:bold; border-bottom:1px solid #ddd;">End Date</td>
                <td style="padding:8px; border-bottom:1px solid #ddd;">{self.end_date}</td>
            </tr>
            <tr>
                <td style="padding:8px; font-weight:bold; border-bottom:1px solid #ddd;">Total Amount</td>
                <td style="padding:8px; border-bottom:1px solid #ddd;">₹ {self.total_amount}</td>
            </tr>
        </table>

        <div style="text-align:center; margin-top:20px;">
            <a href="{frappe.utils.get_url()}/app/scholarship/{self.name}" 
               style="background:#2e7d32; color:white; padding:10px 20px; 
                      text-decoration:none; border-radius:5px; font-weight:bold;">
                View Scholarship
            </a>
        </div>

        <p style="font-size:13px; color:#777; margin-top:20px; text-align:center;">
            This is an automated message from Scholarship Management System.
        </p>
    </div>
</div>
"""


            frappe.sendmail(
                recipients=users,
                subject=subject,
                message=message,
                now=True
            )
    def validate(self):
        scholarship_name = self.name1
        max_applicants = frappe.db.count('Scholarship Application', {
            'scholarship_name': scholarship_name
        })

        current_date = getdate()
        start_date = getdate(self.start_date)
        end_date = getdate(self.end_date)

        if start_date <= current_date <= end_date and max_applicants < self.max_applicants_allowed:
            self.status = "Active"
        else:
            self.status = "Closed"

        self.created_by = frappe.session.user
	



@frappe.whitelist()
def get_applicant_name():
	user_email = frappe.db.get_value("User", frappe.session.user, "email")
	if not user_email:
		frappe.throw("User email not found.")
	applicant = frappe.db.get_value("Applicant Profile", {"email": user_email}, "name")
	# if not applicant:
	# 	frappe.throw("No Applicant Profile found for this user.")
		
	return applicant

def get_permission_query_conditions(user):
	user_email = frappe.db.get_value("User", frappe.session.user, "email")
	if not user_email:
		frappe.throw("User email not found.")
	if "System Manager" in frappe.get_roles(user):
		return None
	elif "Student" in frappe.get_roles(user):
		return "`tabScholarship`.`status` = 'Active'" 

@frappe.whitelist()
def eligibility_criteria(scholarship_name=None):
    user_email = frappe.db.get_value("User", frappe.session.user, "email")
    applicant_name = frappe.db.get_value("Applicant Profile", {"email": user_email}, "name")

    if not applicant_name:
        return False

    applicant = frappe.get_doc("Applicant Profile", applicant_name)
    scholarship = frappe.get_doc("Scholarship", scholarship_name)

    if not scholarship or not applicant:
        return False

    if scholarship.caste:
        caste_values = [row.caste_name for row in scholarship.caste]   
    if applicant.caste not in caste_values:
        return False

    if scholarship.cgpa and applicant.cgpa < scholarship.cgpa:
        print(applicant.cgpa)
        print(scholarship.cgpa)
        return False

    if scholarship.income and applicant.income < scholarship.income:
        print(scholarship.income)
        print(applicant.income)
        return False

    
    if scholarship.tenth_mark and applicant.tenth_mark < scholarship.tenth_mark:
        return False

    if scholarship.eleventh_mark and applicant.eleventh_mark < scholarship.eleventh_mark:
        return False

    if scholarship.twelfth_mark and applicant.twelfth_mark < scholarship.twelfth_mark:
        return False

    return True
