// Copyright (c) 2025, sanjesh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Verification Checklist", {
	refresh(frm) {
        frm.set_query('application', () => {
            return {
                filters: {
                    docstatus: '1'
                }
            };
        });

	},
});
