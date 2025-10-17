import frappe
import re
from scholarship_management.scholarship_management.doctype.scholarship_application.scholarship_application import auto_fill


@frappe.whitelist()
def chatbot_reply(message, user=None):

    user_message = message.strip().lower()

    if re.search(r"\b(hello|hi|hii)\b", user_message):
        return ["Hi there!  How can I help you today?"]

    elif "help" in user_message:
        return ["I can help you with Scholarship navigation, document creation, and reports."]

    # List scholarships
    elif  "scholarship list" in user_message:
        scholarships = frappe.get_all(
            "Scholarship",
            filters={"status": "Active"},
            fields=["name1", "start_date", "end_date", "total_amount"],
            order_by="start_date asc"
        )

        if not scholarships:
            return ["Currently, there are no open scholarships."]

        messages = [" Available Scholarships:"]
        for s in scholarships:
            messages.append(
                f"• {s.name1} — ₹{s.total_amount} (From {s.start_date} to {s.end_date})"
            )
        return messages

        # Apply for scholarship
    elif user_message.startswith("apply "):
        scholarship_name = message[6:].strip()  
        scholarship = frappe.get_all(
            "Scholarship",
            filters={"name1": scholarship_name, "status": "Active"},
            fields=["name1", "name"]
        )

        if not scholarship:
            return [f" Sorry, scholarship '{scholarship_name}' is not available or not active."]

        scholarship_docname = scholarship[0]["name"]

        current_user = frappe.session.user
        user_email = frappe.db.get_value("User", current_user, "email")
        applicant_id = frappe.db.get_value("Applicant Profile", {"email": user_email}, "name")

        if not applicant_id:
            return [" No Applicant Profile found for your account. Please create one first."]

        # Check if already applied
        existing_application = frappe.get_all(
            "Scholarship Application",
            filters={
                "scholarship_name": scholarship_docname,
                "applicant": applicant_id
            },
            fields=["name"]
        )
        if existing_application:
            return [f" You have already applied for '{scholarship_name}'!"]

        # Run auto_fill to pre-populate data
        auto_data = auto_fill(scholarship_docname)

        # Create Scholarship Application
        application_data = {
            "doctype": "Scholarship Application",
            "scholarship_name": scholarship_docname,
            "applicant": applicant_id,
            "status": "Applied"
        }
        application_data.update(auto_data)  
        application = frappe.get_doc(application_data)
        application.insert(ignore_permissions=True)
        frappe.db.commit()

        return [f"Your application for '{scholarship_name}' has been submitted successfully with required documents auto-attached!"]
    
        # Check scholarship status
    elif "my applications status" in user_message:
        apps = get_my_applications()
        if not apps:
            return [" You have not applied for any scholarships yet."]
        
        messages = ["Your current scholarship applications:"]
        for app in apps:
            messages.append(f"{app['scholarship_name']} → Status: {app['status']}")
        return messages
    elif user_message.startswith("status "):
        scholarship_name = message[7:].strip()  
        if not scholarship_name:
            return ["Please provide the scholarship name. Example: status Chief Minister’s Merit Scholarships"]

        # Call your function
        result = get_scholarship_status(scholarship_name)

        if "error" in result:
            return [f" {result['error']}"]
        elif result["status"] == "Not applied":
            return [f" You have not applied for '{scholarship_name}'."]
        else:
            return [f"Your application for '{scholarship_name}' is current Status '{result['status']}' (applied on {result['application_date']})."]

    # Check scholarship details
    elif user_message.startswith("scholarship "):
        # Extract scholarship name after "scholarship "
        scholarship_name = message[11:].strip()  
        if not scholarship_name:
            return [" Please provide the scholarship name. Example: scholarship Chief Minister’s Merit Scholarships"]

        scholarship = frappe.get_all(
            "Scholarship",
            filters={"name1": scholarship_name},
            fields=["name1", "start_date", "end_date", "total_amount", "eligibility_criteria", "status"]
        )

        if not scholarship:
            return [f"Scholarship '{scholarship_name}' not found."]

        s = scholarship[0]
        details = (
            f" Scholarship Details:\n"
            f"• Name: {s['name1']}\n"
            f"• Status: {s['status']}\n"
            f"• Total Amount: ₹{s['total_amount']}\n"
            f"• Start Date: {s['start_date']}\n"
            f"• End Date: {s['end_date']}\n"
            f"• Eligibility: {s['eligibility_criteria']}"
        )
        return [details]




    elif "bye" in user_message:
        return ["Goodbye! Have a great day! "]

    else:
        return [f"We Couldn’t Find What You’re Looking For"]


def get_my_applications():
    user_email = frappe.db.get_value("User", frappe.session.user, "email")
    if not user_email:
        return []

    applicant_name = frappe.db.get_value("Applicant Profile", {"email": user_email}, "name")
    if not applicant_name:
        return []

    applications = frappe.get_all(
        "Scholarship Application",
        filters={"applicant": applicant_name},
        fields=["scholarship_name", "status", "application_date"],
        order_by="creation desc"
    )

    return applications



def get_scholarship_status(scholarship_name):
    """
    Get current user's application status for a particular scholarship
    """
    user_email = frappe.db.get_value("User", frappe.session.user, "email")
    if not user_email:
        return {"error": "User email not found"}

    applicant_name = frappe.db.get_value("Applicant Profile", {"email": user_email}, "name")
    if not applicant_name:
        return {"error": "Applicant profile not found"}

    application = frappe.get_all(
        "Scholarship Application",
        filters={
            "applicant": applicant_name,
            "scholarship_name": scholarship_name
        },
        fields=["status", "application_date"]
    )

    if not application:
        return {"status": "Not applied"}

    # If multiple applications exist, return latest
    latest = sorted(application, key=lambda x: x["application_date"], reverse=True)[0]
    return {
        "status": latest["status"],
        "application_date": latest["application_date"]
    }
