import frappe

def get_context(context):
    context.sponsors = frappe.get_all(
        "Sponsor",
        fields=["name", "email"]
    )

    return context

