# scholarship_management/utils.py
import frappe

def get_home_page(user=None):
    user = user or frappe.session.user
    roles = frappe.get_roles(user)

    if "Administrator" in roles:
        return "/app/dashboard-view/Admin"  # admin page
    elif "Student" in roles:
        return "/app/my-dashboard"          # student page
    else:
        return "/app"                        # default page
