# Copyright (c) 2025, sanjesh and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestSample(FrappeTestCase):

    def setUp(self):
        """Set up test data before each test runs."""
        self.test_scholarship = frappe.get_doc({
            "doctype": "Sample",
        	"name1": "Test Scholarship",
        	"total_amount": 5000,
        })
        self.test_scholarship.save()

    def tearDown(self):
        """Clean up after each test."""
        frappe.delete_doc("Sample", self.test_scholarship.name)

    def test_scholarship_creation(self):
        """Test that a Scholarship record is created correctly."""
        scholarship = frappe.get_doc("Sample", self.test_scholarship.name)
        self.assertEqual(scholarship.name1, "Test Scholarship")
        self.assertEqual(scholarship.total_amount, 5000)

    def test_scholarship_field_defaults(self):
        """Test that default fields are set correctly."""
        scholarship = frappe.get_doc("Sample", self.test_scholarship.name)
        self.assertIsNotNone(scholarship.creation)
        self.assertEqual(scholarship.docstatus, 0)

    def test_duplicate_prevention(self):
        """Ensure duplicate scholarships are not allowed."""
        duplicate = frappe.new_doc("Sample")
        duplicate.name1 = "Test Scholarship"
        duplicate.total_amount = 5000
        with self.assertRaises(frappe.DuplicateEntryError):
            duplicate.insert()