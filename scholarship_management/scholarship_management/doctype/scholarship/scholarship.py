import frappe
import re
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import getdate

class Scholarship(WebsiteGenerator):
    def after_insert(self):
        frappe.enqueue(send_scholarship_email, scholarship_name=self.name1,start_date=self.start_date,end_date=self.end_date,total_amount=self.total_amount,name=self.name)
    def send_scholarship_email(scholarship_name,start_date,end_date,total_amount,name):
        users = frappe.get_all("User", filters={"enabled": 1,"role":"Student"}, pluck="email")
        if users:
            subject = f"🎓 New Scholarship Created: {scholarship_name}"
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
                <td style="padding:8px; border-bottom:1px solid #ddd;">{scholarship_name}</td>
            </tr>
            <tr>
                <td style="padding:8px; font-weight:bold; border-bottom:1px solid #ddd;">Start Date</td>
                <td style="padding:8px; border-bottom:1px solid #ddd;">{start_date}</td>
            </tr>
            <tr>
                <td style="padding:8px; font-weight:bold; border-bottom:1px solid #ddd;">End Date</td>
                <td style="padding:8px; border-bottom:1px solid #ddd;">{end_date}</td>
            </tr>
            <tr>
                <td style="padding:8px; font-weight:bold; border-bottom:1px solid #ddd;">Total Amount</td>
                <td style="padding:8px; border-bottom:1px solid #ddd;">₹ {total_amount}</td>
            </tr>
        </table>

        <div style="text-align:center; margin-top:20px;">
            <a href="{frappe.utils.get_url()}/app/scholarship/{name}" 
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

        send_email_new_scholarship=frappe.db.get_single_value("Scholarship Settings","send_email_new_scholarship")
        if send_email_new_scholarship == 1:
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

        if start_date <= current_date <= end_date and max_applicants < int(self.max_applicants_allowed):
            self.status = "Active"
        elif current_date <= start_date:
            self.status = "Upcoming"
        else:
            self.status = "Closed"
        self.created_by = frappe.session.user


    def before_save(self):
        total = self.total_amount or 0
        doc_before_save = self.get_doc_before_save()
        old_rows_by_name = {row.name: row for row in doc_before_save.add_on}
        print(old_rows_by_name)
        for row in self.add_on:
            old_row = old_rows_by_name.get(row.name)
            print(old_row)
            if old_row:
                total -= old_row.total_price or 0
            total += row.total_price or 0 
        self.total_amount = total


   
                







@frappe.whitelist()
def get_applicant_name():
	user_email = frappe.db.get_value("User", frappe.session.user, "email")
	if not user_email:
		frappe.throw("User email not found.")
	applicant = frappe.db.get_value("Applicant Profile", {"email": user_email}, "name")
	return applicant

def get_permission_query_conditions(user):
    user_email = frappe.db.get_value("User", frappe.session.user, "email")
    if not user_email:
        frappe.throw("User email not found.")
    if "System Manager" in frappe.get_roles(user):
        return None
    elif "Student" in frappe.get_roles(user):
        return "`tabScholarship`.`status` IN ('Active', 'Upcoming')"

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

@frappe.whitelist()
def caste_allocated(total_applications,scholarship_name):
    user = frappe.session.user
    email = frappe.db.get_value("User", {"name": user}, "email")
    caste_name = frappe.db.get_value("Applicant Profile", {"email": email}, "caste")

    if not caste_name:
        print("Caste not found → Returning True (block user).")
        return True  

    doc = frappe.get_doc("Scholarship Settings", "Scholarship Settings")
    caste_distribution = {}
    total_applications = int(total_applications)
    total_allocated = 0
    sc_key = None

    for row in doc.caste_allocate:
        caste_key = row.caste_name.strip().lower()
        percentage = float(row.percentage or 0)
        count = round(total_applications * percentage / 100)
        caste_distribution[caste_key] = count
        total_allocated += count

        if caste_key == "sc":
            sc_key = caste_key

    if total_allocated != total_applications and sc_key:
        remaining = total_applications - total_allocated
        caste_distribution[sc_key] += remaining
        print(f"Adjusted SC count by {remaining} to fix rounding mismatch.")

    actual_data = frappe.db.sql("""
    SELECT LOWER(TRIM(ap.caste)) AS caste, COUNT(sa.name) AS total_applications
    FROM `tabScholarship Application` sa
    JOIN `tabApplicant Profile` ap ON sa.applicant = ap.name
    WHERE sa.scholarship_name = %s
    GROUP BY caste
""", (scholarship_name,), as_dict=True)

    actual_data_dict = {row['caste']: row['total_applications'] for row in actual_data}
    user_caste = caste_name.strip().lower()

    used = actual_data_dict.get(user_caste, 0)
    allowed = caste_distribution.get(user_caste, 0)

    result = True if used >= allowed else False
    print(f"Caste: {user_caste}, Used: {used}, Allowed: {allowed}, Result: {result}")



    return result
