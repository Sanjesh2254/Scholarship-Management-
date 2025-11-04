import frappe
from frappe.utils import today, add_years
from frappe.core.doctype.user.user import get_system_users
import frappe
from frappe.utils import today, add_years, getdate
@frappe.whitelist()
def send_one_year_old_applicant_update_email():
    one_year_ago = add_years(getdate(today()), -1)
    applicants = frappe.get_all("Applicant Profile", filters={"update_date": ("<", one_year_ago)})

    for applicant in applicants:
        email = "sanjeshtridots@gmail.com"
        print(email)
        subject = "🔔 Please Update Your Profile"
        html_message = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; 
                    border: 1px solid #e0e0e0; border-radius: 10px; background: #fafafa;">

            <h2 style="color: #2c3e50; text-align: center;">Update Your Profile</h2>
            <p style="font-size: 15px; color: #555;">
                Hello,
            </p>
            <p style="font-size: 15px; color: #555;">
                Our records show that your profile hasn’t been updated since 
                <b style="color: #d35400;">{one_year_ago}</b>. 
            </p>
            <p style="font-size: 15px; color: #555;">
                Please take a moment to update your details to continue enjoying all benefits.
            </p>

            <div style="text-align: center; margin-top: 20px;">
                <a href="http://127.0.0.1:8007/app/applicant-profile" 
                style="background: Green; color: white; text-decoration: none; 
                        padding: 12px 25px; border-radius: 6px; font-size: 15px;">
                    Update Now
                </a>
            </div>

            <p style="font-size: 13px; color: #888; margin-top: 30px; text-align: center;">
                If you have already updated your profile, you can ignore this message.  
            </p>
        </div>
        """



        if email:
            frappe.sendmail(
                recipients=[email],
                subject=subject,
                message=html_message,
                now=True
            )
    print("SDRG",applicants)

