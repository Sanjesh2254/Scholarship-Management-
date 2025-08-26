// Copyright (c) 2025, sanjesh and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Scholarship", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Scholarship', {
    
    start_date: function(frm) {
        const selected_date = frm.doc.start_date;
        const today = frappe.datetime.get_today();

        if (selected_date < today) {
            frappe.msgprint(__('Start Date cannot be in the past'));
            frm.set_value('start_date', null);
        }
    },
    end_date: function(frm) {
        const start_date = frm.doc.start_date;
        const end_date = frm.doc.end_date;
        if (end_date < start_date) {
            frappe.msgprint(__('End Date cannot be earlier than Start Date'));
            frm.set_value('end_date', null);
        }
    },
    

    refresh: function (frm) {
        
        if (!frm.is_new() && frm.doc.status === "Active") {
            frappe.call({
                method: "scholarship_management.scholarship_management.doctype.scholarship.scholarship.eligibility_criteria",
                args: { scholarship_name: frm.doc.name },
                callback: function (r) {
                    if (r.message === true) {
                        // Show Apply button only if eligible
                        frm.add_custom_button("Apply for Scholarship", function () {
                            frappe.call({
                                method: 'scholarship_management.scholarship_management.doctype.scholarship.scholarship.get_applicant_name',
                                callback: function (res) {
                                    if (res.message) {
                                        let applicant_name = res.message;
                                        frappe.call({
                                            method: 'scholarship_management.scholarship_management.doctype.scholarship_application.scholarship_application.check_existing_application',
                                            args: {
                                                scholarship_name: frm.doc.name,
                                                applicant: applicant_name
                                            },
                                            callback: function (res2) {
                                                if (res2.message === true) {
                                                    frappe.msgprint(__('You have already applied for this scholarship.'));
                                                } else {
                                                    frappe.new_doc('Scholarship Application', {
                                                        scholarship_name: frm.doc.name,
                                                        applicant: applicant_name
                                                    });
                                                }
                                            }
                                        });
                                    } else {
                                        frappe.msgprint('Applicant not found for current user.');
                                        frappe.new_doc('Applicant Profile');
                                    }
                                }
                            });
                        });
                    } else {
                        // Not eligible → don’t show the button
                        frm.dashboard.set_headline(__('You are not eligible for this scholarship.'));
                    }
                }
            });
        }
        if (frappe.user.has_role("System Manager")) {
            let fields = ["cgpa", "income", "tenth_mark", "eleventh_mark", "twelfth_mark", "caste"];
            fields.forEach(field => {
                frm.set_df_property(field, "hidden", 0); // always visible
            });
            return; // stop here for admin
        }
        // Run only for Students
        if (frappe.user.has_role("Student")) {
            // List of eligibility fields you want to hide if empty/06
            let fields = ["cgpa", "income", "tenth_mark", "eleventh_mark", "twelfth_mark"];

            fields.forEach(field => {
                let value = frm.doc[field];

                if (value && value != 0) {
                    frm.set_df_property(field, "hidden", 0); // show
                } else {
                    frm.set_df_property(field, "hidden", 1); // hide
                }
            });

            // Special handling for caste (multiselect / table field)
            if (frm.doc.caste && frm.doc.caste.length > 0) {
                frm.set_df_property("caste", "hidden", 0);
            } else {
                frm.set_df_property("caste", "hidden", 1);
            }
        }
    },

});




