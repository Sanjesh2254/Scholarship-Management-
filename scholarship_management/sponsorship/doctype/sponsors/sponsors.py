# Copyright (c) 2025, sanjesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Sponsors(Document):
	pass

@frappe.whitelist()
def send_sponsor_reminders():
    if not frappe.db.get_single_value("Scholarship Settings", "enable_sponsor_reminders"):
        return

    sponsors = frappe.get_all("Sponsor", fields=["name", "email"])
    for sponsor in sponsors:
        frappe.sendmail(
            recipients=sponsor.email,
            subject="Scholarship Fund Reminder",
            message="This is a monthly reminder to release scholarship funds."

        )



