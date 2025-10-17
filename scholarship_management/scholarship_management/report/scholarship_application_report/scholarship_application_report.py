# Copyright (c) 2025, sanjesh and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data)
    report= get_report_summary(data)
    return columns, data, None, chart,report


def get_columns():
	columns=[
		{
                'fieldname': 'scholarship_name',
                'label': _('Scholarship Name'),
                'fieldtype': 'Link',
                'options': 'Scholarship',
				"width": "250px"
            },
			{
				'fieldname':'applicant',
				'label':_('Applicant Name'),
				'fieldtype':'Link',
				'options':'Applicant Profile',
				"width": "250px"

			},
			{
				'fieldname':'status',
				'label':_('Status'),
				'fieldtype':'Select',
				'options':['','Applied','Verified','Approved','Rejected','Paid'],
				"width": "250px"

			},
			{
				'fieldname':'application_date',
				'label':_('Date'),
				'fieldtype':'Date',
				"width": "250px"
			},
			
	]
	
	return columns	

def get_data(filters):
    condition = '1 = 1'
    
    if filters.get("scholarship_name"):
        condition += f" AND S.scholarship_name='{filters.get('scholarship_name')}'"

    if filters.get("applicant"):
        condition += f" AND S.applicant='{filters.get('applicant')}'"

    if filters.get("status"):
        condition += f" AND S.status='{filters.get('status')}'"

    if filters.get("application_date"):
        condition += f" AND S.application_date='{filters.get('application_date')}'"

    query = f"""
        SELECT
            S.scholarship_name,
            S.applicant,
            S.status,
            S.application_date
        FROM
            `tabScholarship Application` S
        WHERE
            {condition}
        ORDER BY S.application_date DESC
    """
    return frappe.db.sql(query,as_dict=True)




def get_chart_data(data):
    status_count = {"Paid": 0, "Rejected": 0}

    for entry in data:
        if entry.get("status") == "Paid":
            status_count["Paid"] += 1
        elif entry.get("status") == "Rejected":
            status_count["Rejected"] += 1

    chart = {
        "data": {
            "labels": ["Approved", "Rejected"],
            "datasets": [
                {
                    "name": "Appointments",
                    "values": [status_count["Paid"], status_count["Rejected"]]
                }
            ]
        },
        "type": "donut",
        "height": 300
    }

    return chart


def get_report_summary(data):
    Paid, Verified, Rejected = 0, 0, 0

    for entry in data:
        status = entry.get("status")
        
        if status == "Verified":
            Verified += 1
        elif status == "Paid":
            Paid += 1
        elif status == "Rejected":
            Rejected += 1

    return [
        {
            "value": Verified,
            "indicator": "Yellow",
            "label": "Verified Application",
            "datatype": "Int"
        },
        {
            "value": Paid,
            "indicator": "Green",
            "label": "Approved Application",
            "datatype": "Int"
        },
        {
            "value": Rejected,
            "indicator": "Red",
            "label": "Rejected Application",
            "datatype": "Int"
        },
    ]
