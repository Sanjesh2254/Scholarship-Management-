frappe.listview_settings['Approval'] = {
    onload(listview) {
        listview.page.add_action_item('💸 Make Payment for Selected', function() {
            let selected = listview.get_checked_items();

            if (!selected.length) {
                frappe.msgprint("Please select at least one record.");
                return;
            }

            selected.forEach(record => {
                frappe.call({
                    method: "frappe.client.get",
                    args: {
                        doctype: "Approval",
                        name: record.name
                    },
                    callback: function(r) {
                        if (!r.exc) {
                            let approval = r.message;

                            if (approval.applicant) {
                                frappe.db.get_doc("Scholarship Application", approval.applicant)
                                    .then(app => {
                                        if (app.scholarship_name) {
                                            frappe.db.get_doc("Scholarship", app.scholarship_name)
                                                .then(scholarship => {
                                                    let amount = (scholarship.total_amount || 0) * 100;

                                                    // Open Razorpay for each record
                                                    frappe.require("https://checkout.razorpay.com/v1/checkout.js", function () {
                                                        let options = {
                                                            key: "rzp_test_1DP5mmOlF5G5ag",
                                                            amount: amount,
                                                            currency: "INR",
                                                            name: "Test Engine",
                                                            description: "Scholarship Payment",
                                                            handler: function (response) {
                                                                let payment_id = response.razorpay_payment_id;
                                                                let paid_amount = amount / 100;

                                                                frappe.call({
                                                                    method: "frappe.client.insert",
                                                                    args: {
                                                                        doc: {
                                                                            doctype: "Transaction",
                                                                            applicant: approval.applicant,
                                                                            scholarship: app.scholarship_name,
                                                                            payment_id: payment_id,
                                                                            paid_amount: paid_amount
                                                                        }
                                                                    },
                                                                    callback: function(r2) {
                                                                        if (!r2.exc) {
                                                                            frappe.show_alert({
                                                                                message: `💾 Transaction created for ${approval.name}`,
                                                                                indicator: 'green'
                                                                            });
                                                                        }
                                                                    }
                                                                });
                                                            }
                                                        };
                                                        let rzp = new Razorpay(options);
                                                        rzp.open();
                                                    });
                                                });
                                        }
                                    });
                            }
                        }
                    }
                });
            });
        });
    }
};
