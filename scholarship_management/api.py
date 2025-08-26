import frappe
import re

@frappe.whitelist()
def chatbot_reply(message, user=None):
    """
    user: optional, pass frappe.session.user if you want to create the application for the logged-in user
    """
    user_message = message.strip().lower()

    # Greetings
    if re.search(r"\b(hello|hi)\b", user_message):
        return ["Hi there! 👋 How can I help you today?"]

    # Status check
    elif "status" in user_message:
        return ["Sure! Please provide your reference number so I can check the status."]

    # Help
    elif "help" in user_message:
        return ["I can help you with ERPNext navigation, document creation, and reports."]

    # List scholarships
    elif "scholarship" in user_message or "scholarship list" in user_message:
        scholarships = frappe.get_all(
            "Scholarship",
            filters={"status": "Active"},
            fields=["name1", "start_date", "end_date", "total_amount","eligibility_criteria"],
            order_by="start_date asc"
        )

        if not scholarships:
            return ["Currently, there are no open scholarships."]

        messages = ["📋 Available Scholarships:"]
        for s in scholarships:
            messages.append(
                f"• {s.name1} — ₹{s.total_amount} (From {s.start_date} to {s.end_date} {s.eligibility_criteria})"
            )
        return messages

    # Apply for scholarship
    elif user_message.startswith("apply "):
        # Extract scholarship name after "apply"
        scholarship_name = message[6:].strip()  # Preserve original case
        scholarship = frappe.get_all(
            "Scholarship",
            filters={"name1": scholarship_name, "status": "Active"},
            fields=["name1"]
        )

        if not scholarship:
            return [f"Sorry, scholarship '{scholarship_name}' is not available or not active."]

        # Create Scholarship Application
        current_user = frappe.session.user
        applicant_id = frappe.db.get_value("Applicant Profile", {"email": current_user}, "name")
        application = frappe.get_doc({
            "doctype": "Scholarship Application",
            "scholarship_name": scholarship_name,
            "applicant": applicant_id,
            "status": "Applied"
        })
        application.insert()
        frappe.db.commit()

        return [f"✅ Your application for '{scholarship_name}' has been submitted successfully!"]

    # Goodbye
    elif "bye" in user_message:
        return ["Goodbye! Have a great day! 😊"]

    # Default reply
    else:
        return [f"You said: {message}"]
