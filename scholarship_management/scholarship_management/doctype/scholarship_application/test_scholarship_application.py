# Copyright (c) 2025, sanjesh and Contributors
# See license.txt

# # import frappe
# from frappe.tests.utils import FrappeTestCase


# class TestScholarshipApplication(FrappeTestCase):
# 	pass



import frappe
from frappe.tests.utils import FrappeTestCase

class TestScholarshipApplication(FrappeTestCase):

    def setUp(self):
        frappe.set_user("Administrator")

    def create_test_application(self, **overrides):
        default_data = {
            "doctype": "Scholarship Application",
            "applicant_name": "John Doe",
            "email": "john@example.com",
            "gpa": 3.7,
            "course": "Computer Science"
        }
        default_data.update(overrides)
        app = frappe.get_doc(default_data)
        app.insert()
        return app

    def test_application_creation(self):
        """Ensure a valid application can be created"""
        app = self.create_test_application()
        self.assertEqual(app.applicant_name, "John Doe")
        self.assertTrue(app.name)

    def test_email_validation(self):
        """Ensure invalid emails are rejected"""
        app = frappe.get_doc({
            "doctype": "Scholarship Application",
            "applicant_name": "Test User",
            "email": "invalid-email",  # Invalid
            "gpa": 3.8,
            "course": "Science"
        })
        with self.assertRaises(frappe.ValidationError):
            app.validate()

    def test_gpa_eligibility_check(self):
        """Ensure GPA below 3.0 is rejected"""
        app = frappe.get_doc({
            "doctype": "Scholarship Application",
            "applicant_name": "Low GPA Student",
            "email": "lowgpa@example.com",
            "gpa": 2.5,  # Below minimum
            "course": "Arts"
        })
        with self.assertRaises(frappe.ValidationError):
            app.validate()

    def test_status_update(self):
        """Ensure status can be updated and saved"""
        app = self.create_test_application()
        app.status = "Approved"
        app.save()
        updated = frappe.get_doc("Scholarship Application", app.name)
        self.assertEqual(updated.status, "Approved")
