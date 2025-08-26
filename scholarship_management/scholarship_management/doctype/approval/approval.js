// Copyright (c) 2025, sanjesh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Approval", {
	refresh(frm) {
         // Trigger payment automatically if status = Approved and no payment yet
    if (frm.doc.status === "Approved" && !frm.doc.payment_id) {
        frappe.db.get_doc("Scholarship Application", frm.doc.applicant)
            .then(app => {
                if (app.scholarship_name) {
                    frappe.db.get_doc("Scholarship", app.scholarship_name)
                        .then(scholarship => {
                            let amount = (scholarship.total_amount || 0) * 100; // in paise

                            // ✅ Check if Transaction already exists for this applicant + scholarship
                            frappe.call({
                                method: "frappe.client.get_list",
                                args: {
                                    doctype: "Transaction",
                                    filters: {
                                        applicant: frm.doc.applicant,
                                        scholarship: app.scholarship_name
                                    },
                                    fields: ["name", "payment_id"],
                                    limit_page_length: 1
                                },
                                callback: function(res) {
                                    if (res.message && res.message.length > 0) {
                                        frappe.msgprint("⚠️ Transaction already exists. Payment not triggered again.");
                                        return;
                                    }

                                    // No transaction yet → proceed with Razorpay
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

                                                // ✅ Create Transaction record
                                                frappe.call({
                                                    method: "frappe.client.insert",
                                                    args: {
                                                        doc: {
                                                            doctype: "Transaction",
                                                            applicant: frm.doc.applicant,
                                                            scholarship: app.scholarship_name,
                                                            payment_id: payment_id,
                                                            paid_amount: paid_amount,
                                                        }
                                                    },
                                                    callback: function(r) {
                                                        if (!r.exc) {
                                                            frappe.msgprint("💾 Transaction created successfully!");
                                                            frm.reload_doc(); // refresh form with updated values
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
            });
    }
        frm.set_query('verified_application', () => {
            return {
                filters: {
                    all_documents_valid: '1'
                }
            };
        });
	},
    verified_application(frm) {
        if (!frm.doc.verified_application) return;

        frappe.call({
            method: "scholarship_management.scholarship_management.doctype.approval.approval.get_applicant",
            args: {
                verification_id: frm.doc.verified_application
            },
            callback: function(r) {
                if (r.message) {
                    frm.set_query('applicant', () => {
                        return {
                            filters: {
                                name: r.message  
                            }
                        };
                    });
                    frm.set_value("applicant", r.message);
                }
            }
        });
    }
});
