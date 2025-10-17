import frappe
import uuid

def execute():
    results = frappe.db.sql("""
        SELECT name FROM `tabApplicant Profile`
        WHERE application_code IS NULL OR application_code = ''
    """, as_dict=True)

    for row in results:
        code = str(uuid.uuid4())[:8].upper()

        frappe.db.set_value('Applicant Profile', row.name, 'application_code', code)

    frappe.db.commit()
