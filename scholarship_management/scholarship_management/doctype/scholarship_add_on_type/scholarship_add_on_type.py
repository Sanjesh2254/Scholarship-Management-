# Copyright (c) 2025, sanjesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ScholarshipAddonType(Document):
	def before_save(self):
		doc = frappe.get_doc("Scholarship Add-on", {"name1": self.add_on_name})
		print( self.amount)
		print( doc.applicable_months)
		old_amount=doc.price *doc.applicable_months
		amount=  doc.applicable_months * self.amount
		frappe.db.set_value("Scholarship Add-on", {"name1": self.add_on_name}, "price", self.amount)

		frappe.db.set_value("Scholarship Add-on", {"name1": self.add_on_name}, "total_price", amount)
		scholarships = frappe.get_all("Scholarship", fields=["name", "total_amount"])
		for s in scholarships:
			scholarship_doc = frappe.get_doc("Scholarship", s.name)
			for addon_row in scholarship_doc.add_on:
				if addon_row.name1 == self.add_on_name:
					new_total = ((scholarship_doc.total_amount or 0)-old_amount) + amount
					frappe.db.set_value("Scholarship", s.name, "total_amount", new_total)
				

			