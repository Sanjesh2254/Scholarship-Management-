// Copyright (c) 2025, sanjesh and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Scholarship Renewal", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Scholarship Renewal', {
  refresh: function(frm) {
        frm.$wrapper.find(".form-section .form-group label").css("color", "#10b035ff");

    
        frm.set_query("scholarship_name", () => {
            return {
                filters: {
                    status:"Paid",
                    scholarship_name: ["in", get_allowed_scholarships()]
                }
            };
        });

    if (frm.doc.status === "Paid" && !frm.doc.payment_id) {
        let scholarship_app_name = frm.doc.scholarship_name;
        let applicant = frm.doc.applicant;

        if (scholarship_app_name && applicant) {
            // Get Scholarship Application
            frappe.db.get_doc("Scholarship Application", scholarship_app_name)
                .then(scholarship_application => {
                    console.log("Scholarship Application Name:", scholarship_app_name);
                    let scholarship_name = scholarship_application.scholarship_name;
                    console.log("Linked Scholarship:", scholarship_name);

                    // Get Scholarship Document
                    return frappe.db.get_doc("Scholarship", scholarship_name);
                })
                .then(scholarship => {
                    console.log("Scholarship Doc:", scholarship);

                    let amount = (scholarship.total_amount || 0) * 100;

                    // Check if transaction already exists
                    frappe.call({
                        method: "frappe.client.get_list",
                        args: {
                            doctype: "Transaction",
                            filters: {
                                applicant: applicant,
                                scholarship: scholarship.name,
                                transaction_type:"Renewal"

                            },
                            fields: ["name", "payment_id"],
                            limit_page_length: 1
                        },
                        callback: function(res) {
                            if (res.message && res.message.length > 0) {
                            
                                return;
                            }

                            // Load Razorpay Checkout
                            frappe.require("https://checkout.razorpay.com/v1/checkout.js", function () {
                                let options = {
                                    key: "rzp_test_1DP5mmOlF5G5ag",
                                    amount: amount,
                                    currency: "INR",
                                    name: "Scholarship Portal",
                                    description: "Scholarship Payment",
                                    handler: function (response) {
                                        let payment_id = response.razorpay_payment_id;
                                        let paid_amount = amount / 100;

                                        frappe.msgprint("✅ Payment successful. Payment ID: " + payment_id);

                                        // Create Transaction
                                        frappe.call({
                                            method: "frappe.client.insert",
                                            args: {
                                                doc: {
                                                    doctype: "Transaction",
                                                    applicant: applicant,
                                                    scholarship: scholarship.name,
                                                    transaction_type:"Renewal",
                                                    payment_id: payment_id,
                                                    paid_amount: paid_amount,
                                                }
                                            },
                                            callback: function(r) {
                                                if (!r.exc) {
                                                    frappe.msgprint("💾 Transaction created successfully!");
                                                    frm.reload_doc();
                                                } else {
                                                    frappe.msgprint("❌ Failed to create transaction.");
                                                }
                                            }
                                        });
                                    },
                                    theme: {
                                        color: "#54c1f3ff"
                                    }
                                };
                                let rzp = new Razorpay(options);
                                rzp.open();
                            });
                        }
                    });
                })
                .catch(error => {
                    console.error("❌ Error fetching documents:", error);
                    frappe.msgprint("Error fetching scholarship details.");
                });
        }
    }

      
   

   


        
        

      
    },
    scholarship_name: function (frm) {
        check_existing(frm);
    },
    applicant: function (frm) {
        check_existing(frm);    
    },
    scholarship_name: function (frm) {
        
        if (frm.doc.scholarship_name) {
            frappe.call({
                method: "scholarship_management.scholarship_management.doctype.scholarship_renewal.scholarship_renewal.auto_fill",
                args: {
                    scholarship_name: frm.doc.scholarship_name
                },
                callback: function (r) {
                    if (r.message) {
                        let data = r.message;

                        frm.set_value("applicant", data.applicant || "");

                        if (data.community_certificate) {
                            frm.set_value("community_certificate", data.community_certificate);
                        }
                        else{
                                frm.set_df_property("community_certificate", "hidden", 1);

                        }
                        if (data.previous_semester_marksheet) {
                            frm.set_value("previous_semester_marksheet", data.previous_semester_marksheet);
                        }
                        else{
                                frm.set_df_property("previous_semester_marksheet", "hidden", 1);

                        }
                        if (data.tamil_medium_certificate) {
                            frm.set_value("tamil_medium_certificate", data.tamil_medium_certificate);
                        }
                        else{
                                frm.set_df_property("tamil_medium_certificate", "hidden", 1);

                        }
                        if (data.passbook) {
                            frm.set_value("passbook", data.passbook);
                        }
                        if (data.income_certificate) {
                            frm.set_value("income_certificate", data.income_certificate);
                        }
                        else{
                                frm.set_df_property("income_certificate", "hidden", 1);

                        }
                        if (data.tenth_marksheet) {
                            frm.set_value("tenth_marksheet", data.tenth_marksheet);
                        }
                        else{
                                frm.set_df_property("tenth_marksheet", "hidden", 1);

                        }
                        if (data.eleventh_marksheet) {
                            frm.set_value("eleventh_marksheet", data.eleventh_marksheet);
                        }
                        else{
                                frm.set_df_property("eleventh_marksheet", "hidden", 1);

                        }
                        if (data.twelfth_marksheet) {
                            frm.set_value("twelfth_marksheet", data.twelfth_marksheet);
                        }
                        else{
                                frm.set_df_property("twelfth_marksheet", "hidden", 1);

                        }

                        frm.refresh_fields();
                    }
                }
            });
        }
    }


});

function check_existing(frm) {
    if (frm.doc.scholarship_name && frm.doc.applicant) {
        frappe.call({
            method: "scholarship_management.scholarship_management.doctype.scholarship_renewal.scholarship_renewal.check_existing_application",
            args: {
                scholarship_name: frm.doc.scholarship_name,
                applicant: frm.doc.applicant
            },
            callback: function (r) {
                if (r.message) {
                    frappe.msgprint(__("You have already Renewal for this scholarship."));
                    frm.set_value("scholarship_name", "");
                }
            }
        });
    }
};


function get_allowed_scholarships() {
    let allowed = [];
    frappe.call({
        method: "scholarship_management.scholarship_management.doctype.scholarship_renewal.scholarship_renewal.get_allowed_scholarships",
        async: false,
        callback: function (r) {
            if (r.message) {
                allowed = r.message;
            }
        }
    });
    return allowed;
}
