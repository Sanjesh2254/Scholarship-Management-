# Copyright (c) 2025, sanjesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today


class Approval(Document):
	def before_save(self):
		self.approved_date=today()
		self.approved_by=frappe.session.user
	

@frappe.whitelist()
def get_applicant(verification_id):
    verification_doc = frappe.get_doc("Verification Checklist", verification_id)
    return verification_doc.application



