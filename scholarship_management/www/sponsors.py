import frappe

def get_context(context):
    context.sponsors = frappe.get_all(
        "Sponsors",
        fields=["name1", "email"]
    )

    return context

