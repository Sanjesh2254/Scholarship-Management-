import frappe

def get_context(context):
    # Fetch all published scholarships with required fields including 'route'
    context.scholarships = frappe.get_all(
        "Scholarship",
        fields=["name","name1", "total_amount", "start_date", "end_date", "max_applicants_allowed", "status"]
    )
