# Copyright (c) 2025, sanjesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today

class VerificationChecklist(Document):
	def before_save(self):
		self.verification_date=today()
		self.verified_by=frappe.session.user
