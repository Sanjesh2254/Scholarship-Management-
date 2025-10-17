// Copyright (c) 2025, sanjesh and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Scholarship", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Scholarship', {
   
    
    // start_date: function(frm) {
    //     const selected_date = frm.doc.start_date;
    //     const today = frappe.datetime.get_today();

    //     if (selected_date < today) {
    //         frappe.msgprint(__('Start Date cannot be in the past'));
    //         frm.set_value('start_date', null);
    //     }
    // },
    // end_date: function(frm) {
        
    //     const start_date = frm.doc.start_date;
    //     const end_date = frm.doc.end_date;
    //     if (end_date < start_date) {
    //         frappe.msgprint(__('End Date cannot be earlier than Start Date'));
    //         frm.set_value('end_date', null);
    //     }
    // },
    

    refresh: function (frm) {
        frm.add_custom_button('Count', () => {
            let d = new frappe.ui.Dialog({
    title: 'Enter details',
    fields: [
        {
            label: 'Max Applicants Allowed',
            fieldname: 'max_applicants_allowed',
            fieldtype: 'Int'
        }
        
    ],
    size: 'small', 
    primary_action_label: 'Add',
    primary_action(values) {
        frm.set_value('max_applicants_allowed', values.max_applicants_allowed);
        d.hide();
    }
});

d.show();


}, '  + Applicant Count');
        
          frm.set_query("name1", "add_on", function(doc, cdt, cdn) {
                let row = locals[cdt][cdn];

                let selected = (doc.add_on || [])
                    .filter(d => d.name !== row.name)  
                    .map(d => d.name1);    
                    console.log("hii",selected);             

                return {
                    filters: {
                        name: ["not in", selected]
                    }
                };
            });
            frm.set_query("coordinator_name", "coordinator", function(doc, cdt, cdn) {
                let row = locals[cdt][cdn];

                let selected = (doc.coordinator || [])
                    .filter(d => d.name !== row.name)  
                    .map(d => d.coordinator_name);    
                    console.log("hii",selected);             

                return {
                    filters: {
                        name: ["not in", selected]
                    }
                };
            });
            frm.$wrapper.find(".form-section .form-group label").css("color", "#10b035ff");


        
        if (!frm.is_new() && frm.doc.status === "Active") {
    frappe.call({
        method: "scholarship_management.scholarship_management.doctype.scholarship.scholarship.eligibility_criteria",
        args: { scholarship_name: frm.doc.name },
        callback: function (r) {
            if (r.message === true) {
                frappe.call({
                    method: "scholarship_management.scholarship_management.doctype.scholarship.scholarship.caste_allocated",
                    args: { total_applications: frm.doc.max_applicants_allowed,
                        scholarship_name: frm.doc.name
                     },   // pass total applications/quota
                    callback: function (alloc) {
                        if (alloc.message === true) {
                            frm.dashboard.set_headline(__('Your caste quota is already filled. You cannot apply.'));
                        } else {
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
                                                        frm.dashboard.set_headline(__('You have already applied for this scholarship.'));
                                                        frm.remove_custom_button("Apply for Scholarship");
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
                        }
                    }
                });
            } else {
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

            if (frm.doc.caste && frm.doc.caste.length > 0) {
                frm.set_df_property("caste", "hidden", 0);
            } else {
                frm.set_df_property("caste", "hidden", 1);
            }
        }
    },

});


frappe.ui.form.on('Scholarship Add-on', {
    applicable_months: function(frm, cdt, cdn) {
        total_price(frm, cdt, cdn);
    },
    name1: function(frm, cdt, cdn) {
        total_price(frm, cdt, cdn);
    },
    

})
function total_price(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
        row.total_price = row.price * row.applicable_months;
        frm.refresh_field('add_on');
       
}
