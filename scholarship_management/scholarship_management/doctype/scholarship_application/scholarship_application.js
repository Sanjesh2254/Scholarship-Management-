frappe.ui.form.on("Scholarship Application", {
    
    refresh(frm) {
   // Trigger payment automatically if status = Paid and no payment yet
if (frm.doc.status === "Paid" && !frm.doc.payment_id) {
    
    let scholarship_name = frm.doc.scholarship_name;
    let applicant = frm.doc.applicant;

    if (scholarship_name && applicant) {
        frappe.db.get_doc("Scholarship", scholarship_name)
            .then(scholarship => {
                let amount = (scholarship.total_amount || 0) * 100; // in paise

                // ✅ Check if transaction already exists
                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Transaction",
                        filters: {
                            applicant: applicant,
                            scholarship: scholarship_name
                        },
                        fields: ["name", "payment_id"],
                        limit_page_length: 1
                    },
                    callback: function(res) {
                        if (res.message && res.message.length > 0) {
                            return;
                        }

                        // Proceed with Razorpay
                        frappe.require("https://checkout.razorpay.com/v1/checkout.js", function () {
                            let options = {
                                key: "rzp_test_1DP5mmOlF5G5ag",
                                amount: amount,
                                currency: "INR",
                                name: "Scholarship Portal",
                                description: "Scholarship Payment",
                                handler: function (response) {
                                    let payment_id = response.razorpay_payment_id;
                                    let paid_amount = amount / 100; // INR

                                    frappe.msgprint("✅ Payment successful. Payment ID: " + payment_id);

                                    // ✅ Create Transaction
                                    frappe.call({
                                        method: "frappe.client.insert",
                                        args: {
                                            doc: {
                                                doctype: "Transaction",
                                                applicant: applicant,
                                                scholarship: scholarship_name,
                                                payment_id: payment_id,
                                                transaction_type:"Normal",
                                                paid_amount: paid_amount,
                                            }
                                        },
                                        callback: function(r) {
                                            if (!r.exc) {
                                                frappe.msgprint("💾 Transaction created successfully!");
                                                frm.reload_doc();
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
            });
    }
}

         frappe.realtime.on("notification", (message) => {
    frappe.show_alert({
        message: message,
        indicator: 'green'
    });
         });
        frm.set_query('scholarship_name', () => {
            return {
                filters: {
                    status: 'Active'
                }
            };
        });
        
        frappe.call({
            method: 'scholarship_management.scholarship_management.doctype.scholarship.scholarship.get_applicant_name',
            callback: function(r) {
                if (r.message) {
                    frm.set_query('applicant', () => {
                        return {
                            filters: {
                                name: r.message  
                            }
                        };
                    });
                }
            }
        });
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
                method: "scholarship_management.scholarship_management.doctype.scholarship_application.scholarship_application.auto_fill",
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
            method: "scholarship_management.scholarship_management.doctype.scholarship_application.scholarship_application.check_existing_application",
            args: {
                scholarship_name: frm.doc.scholarship_name,
                applicant: frm.doc.applicant
            },
            callback: function (r) {
                if (r.message) {
                    frappe.msgprint(__("You have already applied for this scholarship."));
                    frm.set_value("scholarship_name", "");
                }
            }
        });
    }
};
