// Copyright (c) 2025, sanjesh and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Income Certificate", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Income Certificate', {
    certificate: function(frm) {
        if (frm.doc.certificate) {
            frappe.call({
                method: "scholarship_management.scholarship_management.doctype.income_certificate.income_certificate.extract_income_certificate",
                args: { docname: frm.doc.name },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('extracted_name', r.message.name);
                        frm.set_value('extracted_income', r.message.income);
                        frm.refresh_field(['extracted_name', 'extracted_income']);
                        frappe.msgprint("Details extracted successfully!");
                    }
                }
            });
        }
    }
});

