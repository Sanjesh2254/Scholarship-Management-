import frappe
from frappe import _
from frappe.utils.password import update_password
import smtplib

def is_valid_email_smtp(email):
    """Check if email is valid using SMTP (basic validation)."""
    try:
        domain = email.split('@')[1]
        mx_server = 'gmail-smtp-in.l.google.com'  
        server = smtplib.SMTP()
        server.set_debuglevel(0)
        server.connect(mx_server)
        server.helo(server.local_hostname)  
        server.mail('check@example.com')
        code, _ = server.rcpt(email)
        server.quit()
        return code == 250
    except Exception:
        return False


def get_context(context):
    context.signup_success = False
    context.error_message = None

    context.entered_full_name = frappe.form_dict.get("full_name", "")
    context.entered_email = frappe.form_dict.get("email", "")

    if frappe.form_dict:  
        full_name = frappe.form_dict.get("full_name")
        email = frappe.form_dict.get("email")
        password = frappe.form_dict.get("password")

        try:
            if frappe.db.exists("User", email):
                context.error_message = _("This email is already registered.")
                return context

            if not is_valid_email_smtp(email):
                context.error_message = _("Invalid email. Please check your email address.")
                return context

            user = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": full_name,
                "enabled": 1,
                "user_type": "Website User",
                "roles": [
        {
            "role": "Student"
        }
    ]           
    
            })
            user.insert(ignore_permissions=True)

            update_password(user.name, password)

            frappe.db.commit()
            context.signup_success = True

            context.entered_full_name = ""
            context.entered_email = ""

        except Exception:
            frappe.db.rollback()
            frappe.log_error(frappe.get_traceback(), "Signup Error")
            context.error_message = _("Something went wrong. Please try again.")

    return context
