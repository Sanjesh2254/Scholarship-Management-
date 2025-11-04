# Copyright (c) 2025, sanjesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Sample(Document):
	def autoname(self):
		self.full_name = f"{self.name1}{self.last_name}"


@frappe.whitelist()
def get_full_name(last_name):
	full_name = f"Gokul {last_name}"
	return full_name


