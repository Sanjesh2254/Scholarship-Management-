// Copyright (c) 2025, sanjesh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Transaction", {
 refresh: function (frm) {
                        frm.$wrapper.find(".form-section .form-group label").css("color", "#10b035ff");
        }
});
