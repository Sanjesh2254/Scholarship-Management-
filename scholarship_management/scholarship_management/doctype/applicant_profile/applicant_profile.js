// // Copyright (c) 2025, sanjesh and contributors
// // For license information, please see license.txt

frappe.ui.form.on("Applicant Profile", {

    
        refresh: function (frm) {
                        frm.$wrapper.find(".form-section .form-group label").css("color", "#10b035ff");
                        if (frm.doc.__islocal) return;


        if (frm.doc.website) {
            frm.add_web_link(frm.doc.website, ' View Scholarship List');
        }
        },


    // after_save: function(frm) {
    //     if (frappe.user.has_role("Student")) {
    //         frappe.msgprint("Your profile has been saved successfully.");
    //         setTimeout(function() {
    //             frappe.set_route('List', 'Scholarship');
    //         }, 3000); 
    //     }
    // },
    is_school: function(frm) {
        if (frm.doc.is_school) {
            frm.set_value('college', 0); 
        }
    },
    college: function(frm) {
        if (frm.doc.college) {
            frm.set_value('is_school', 0); 
        }
    },
    class: function(frm) {
        toggle_fields(frm);
    },
    previous_semester_marksheet: function (frm) {
        run_ocr(frm, "previous_semester_marksheet");
    },
    tenthmarksheet: function (frm) {
        run_ocr(frm, "tenthmarksheet");
    },
    eleventhmarksheet: function (frm) {
        run_ocr(frm, "eleventhmarksheet");
    },
    twelfthmarksheet: function (frm) {
        run_ocr(frm, "twelfthmarksheet");
    },
    tenth_marksheet: function (frm) {
        run_ocr(frm, "tenth_marksheet");
    },
    eleventh_marksheet: function (frm) {
        run_ocr(frm, "eleventh_marksheet");
    },
    twelfth_marksheet: function (frm) {
        run_ocr(frm, "twelfth_marksheet");
    },
    community_certificate: function (frm) {
        run_ocr(frm, "community_certificate");
    },
    income_certificate: function (frm) {
        run_ocr(frm, "income_certificate");
    },
    
});

function run_ocr(frm, fieldname) {
    if (!frm.doc[fieldname]) {
        frappe.msgprint(__("Please upload a file first in {0}", [fieldname]));
        return;
    }

    frm.save().then(() => {
        frappe.call({
            method: "scholarship_management.scholarship_management.doctype.applicant_profile.applicant_profile.ocr_text",
            args: {
                docname: frm.doc.name,
                fieldname: fieldname
            },
            freeze: true,
            freeze_message: __("Extracting Data..."),
            callback: function (r) {
                if (!r.exc && r.message) {
                    frappe.show_alert({
                    message: __("Extracted Data: " + JSON.stringify(r.message.ocr_text)),
                    indicator: "green"
                });

                    frm.reload_doc(); 
                }
            }
        });
    });
}



function toggle_fields(frm) {
    if (frm.doc.class == "10") {
        frm.set_df_property("tenth_marksheet", "hidden", 0);
    } else if (frm.doc.class == "11") {
        frm.set_df_property("tenth_marksheet", "hidden", 0);
        frm.set_df_property("eleventh_marksheet", "hidden", 0);
    } else if (frm.doc.class == "12") {
        frm.set_df_property("tenth_marksheet", "hidden", 0);
        frm.set_df_property("eleventh_marksheet", "hidden", 0);
        frm.set_df_property("twelfth_marksheet", "hidden", 0);
    }
}

