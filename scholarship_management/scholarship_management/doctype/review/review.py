# Copyright (c) 2025, sanjesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Review(Document):
	

	def db_insert(self, *args, **kwargs):
		print(f"Simulating insert: {self.name1}, {self.name2}")
		self.__islocal = 0  # Mark as “saved”

	def db_update(self, *args, **kwargs):
		print(f"Simulating update: {self.name1}, {self.name2}")

	def load_from_db(self):
		records = {
			"Virtual-001": {"name1": "First Review", "name2": "Additional Info"},
			"Virtual-002": {"name1": "Second Review", "name2": "Some Notes"},
			"Virtual-003": {"name1": "Third Review", "name2": "Extra Info"},
		}

		if self.name in records:
			self.name1 = records[self.name]["name1"]
			self.name2 = records[self.name]["name2"]
			print(f"name1={self.name1}, name2={self.name2}")
		else:
			self.name1 = ""
			self.name2 = ""
		self.__islocal = 0 
		self._table_fieldnames = [] 

	@staticmethod
	def get_list(args=None):
		return [
			{"name": "Virtual-001", "name1": "First Review", "name2": "Additional Info"},
			{"name": "Virtual-002", "name1": "Second Review", "name2": "Some Notes"},
			{"name": "Virtual-003", "name1": "Third Review", "name2": "Extra Info"},
			{"name": "Virtual-004", "name1": "Third Review", "name2": "Extra Info"}
		]

	@staticmethod
	def get_count(args=None):
		print("Getting count with args:", (len(Review.get_list(args))))
		return len(Review.get_list(args))

	@staticmethod
	def get_stats(args=None):
		reviews = Review.get_list(args)
		print("Calculating stats for reviews:", reviews)
		total = len(reviews)
		print("Total reviews calculated:", total)	
		return {"total": total}



