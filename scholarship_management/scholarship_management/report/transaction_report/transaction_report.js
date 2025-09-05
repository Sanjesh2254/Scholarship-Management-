// Copyright (c) 2025, sanjesh and contributors
// For license information, please see license.txt


frappe.query_reports["Transaction Report"] = {
		"filters": [
		{
                'fieldname': 'scholarship',
                'label': __('Scholarship Name'),
                'fieldtype': 'Link',
                'options': 'Scholarship',
            },
			{
				'fieldname':'payment_id',
				'label':__('Payment Id'),
				'fieldtype':'Data',
			},
			{
				'fieldname':'transaction_type',
				'label':__('Scholarship Type'),
				'fieldtype':'Select',
			},
			{
				'fieldname':'paid_amount',
				'label':__('Paid Amount'),
				'fieldtype':'Int',
			},
			{
				'fieldname':'transaction_date',
				'label':__('Transaction Date'),
				'fieldtype':'Date',
			},

			
	],
};
