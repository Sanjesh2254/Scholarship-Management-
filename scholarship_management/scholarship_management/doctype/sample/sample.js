// Copyright (c) 2025, sanjesh and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Sample", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Sample', {
    refresh(frm) {
        console.log(frm.fields_dict);
        if (frm.doc.currency) {
            if (frm.fields_dict.total_amount) {
                frm.fields_dict.total_amount.set_currency(frm.doc.currency);
            } else {
                console.log("total_amount field not found");
            }
        }
    },
    currency(frm) {
        if (frm.doc.currency && frm.fields_dict.total_amount) {
            frm.fields_dict.total_amount.set_currency(frm.doc.currency);
        }
    }
});

