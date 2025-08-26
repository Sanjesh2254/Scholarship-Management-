# Copyright (c) 2025, sanjesh and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe import _

def execute(filters=None):
    current_user = frappe.session.user
    columns = get_columns(current_user)
    data = get_data(filters, current_user)
    return columns, data


def get_columns(current_user):
    columns = []

    if current_user == "Administrator":
        columns.append({
            'fieldname': 'applicant',
            'label': _('Applicant'),
            'fieldtype': 'Link',
            'options': 'Applicant Profile',
            'width': 200
        })

    columns += [
        {
            'fieldname': 'scholarship',
            'label': _('Scholarship Name'),
            'fieldtype': 'Link',
            'options': 'Scholarship',
            'width': 200
        },
        {
            'fieldname': 'payment_id',
            'label': _('Payment Id'),
            'fieldtype': 'Data',
            'width': 200
        },
        {
            'fieldname': 'transaction_type',
            'label': _('Scholarship Type'),
            'fieldtype': 'Data',
            'width': 200
        },
        {
            'fieldname': 'paid_amount',
            'label': _('Paid Amount'),
            'fieldtype': 'Int',
            'width': 120
        },
        {
            'fieldname': 'transaction_date',
            'label': _('Transaction Date'),
            'fieldtype': 'Date',
            'width': 200
        },
    ]

    return columns


def get_data(filters, current_user):
    if current_user != "Administrator":
        applicant_id = frappe.db.get_value("Applicant Profile", {"email": current_user}, "name")
        condition = f"S.applicant = '{applicant_id}'"
        select_fields = """
            S.scholarship,
            S.payment_id,
            S.transaction_type,
            S.paid_amount,
            S.transaction_date
        """
    else:
        condition = "1=1"
        select_fields = """
            S.applicant,
            S.scholarship,
            S.payment_id,
            S.transaction_type,
            S.paid_amount,
            S.transaction_date
        """

    if filters.get("scholarship"):
        condition += f" AND S.scholarship = '{filters.get('scholarship')}'"

    if filters.get("payment_id"):
        condition += f" AND S.payment_id = '{filters.get('payment_id')}'"

    if filters.get("transaction_type"):
        condition += f" AND S.transaction_type = '{filters.get('transaction_type')}'"

    if filters.get("paid_amount"):
        condition += f" AND S.paid_amount = '{filters.get('paid_amount')}'"

    if filters.get("transaction_date"):
        condition += f" AND S.transaction_date = '{filters.get('transaction_date')}'"

    query = f"""
        SELECT
            {select_fields}
        FROM
            `tabTransaction` S
        WHERE
            {condition}
        ORDER BY S.transaction_date DESC
    """

    return frappe.db.sql(query, as_dict=True)
