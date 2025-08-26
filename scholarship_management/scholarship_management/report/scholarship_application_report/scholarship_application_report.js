// Copyright (c) 2025, sanjesh and contributors
// For license information, please see license.txt

frappe.query_reports["Scholarship Application Report"] = {

	"filters": [
		{
                'fieldname': 'scholarship_name',
                'label': __('Scholarship Name'),
                'fieldtype': 'Link',
                'options': 'Scholarship',
            },
			{
				'fieldname':'applicant',
				'label':__('Applicant Name'),
				'fieldtype':'Link',
				'options':'Applicant Profile',
			},
			{
				'fieldname':'status',
				'label':__('Status'),
				'fieldtype':'Select',
				'options':['','Applied','Verified','Approved','Rejected','Paid'],
			},
			{
				'fieldname':'application_date',
				'label':__('Date'),
				'fieldtype':'Date',
			},
			
	],
	
};



