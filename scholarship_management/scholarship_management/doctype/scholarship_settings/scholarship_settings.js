// Copyright (c) 2025, sanjesh and contributors
// For license information, please see license.txt

frappe.ui.form.on('Scholarship Settings', {
        caste_allocate_remove: function(frm, cdt, cdn) {
        frappe.msgprint(__('A caste allocation row has been removed. Please check the caste allocations'));},
        refresh: function (frm) {
        frm.$wrapper.find(".form-section .form-group label").css("color", "#10b035ff");
         // Hide default sidebar (empty the layout-side-section)
        frm.$wrapper.find(".layout-side-section").empty();

        const is_admin = frappe.user_roles.includes('Administrator');

        const links = is_admin ? `
            <div class="custom-dashboard-link mt-3">
                <a href="http://127.0.0.1:8007/app/dashboard-view/Admin"
                   class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
                   style="margin-top:10px; font-weight:1700;">
                    Dashboard
                </a>
                <a href="http://127.0.0.1:8007/app/scholarship"
                   class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
                   style="margin-top:30px; font-weight:1700;">
                    Scholarship
                </a>
                  <a href="http://127.0.0.1:8007/app/scholarship-application"
                   class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
                   style="margin-top:30px; font-weight:1700;">
                    Application
                </a>
                 <a href="http://127.0.0.1:8007/app/scholarship-renewal"
                   class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
                   style="margin-top:30px; font-weight:1700;">
                    Scholarship Renewal
                </a>
                  <a href="http://127.0.0.1:8007/app/transaction"
                   class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
                   style="margin-top:30px; font-weight:1700;">
                    Transaction
                </a>
                  <a href="http://127.0.0.1:8007/app/report"
                   class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
                   style="margin-top:30px; font-weight:1700;">
                    Report
                </a>
                  <a href="http://127.0.0.1:8007/app/scholarship-settings"
                   class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
                   style="margin-top:30px; font-weight:1700;">
                Scholarship Setting
                </a>
                 <a href="http://127.0.0.1:8007/app/feedback"
                   class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
                   style="margin-top:30px; font-weight:1700;">
                    Feedback
                </a>
            </div>
        ` : `
            <div class="custom-dashboard-link mt-3">
                <a href="http://127.0.0.1:8007/app/my-dashboard"
                   class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
                   style="margin-top:10px; font-weight:1700;">
                    Dashboard
                </a>
                <a href="http://127.0.0.1:8007/app/scholarship"
                   class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
                   style="margin-top:30px; font-weight:1700;">
                    Scholarship
                </a>
                  <a href="http://127.0.0.1:8007/app/scholarship-application"
                   class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
                   style="margin-top:30px; font-weight:1700;">
                    Application
                </a>
                  <a href="http://127.0.0.1:8007/app/scholarship-renewal"
                   class=" btn btn-primary indicator-pill  text-center w-100 d-block"
                   style="margin-top:30px; font-weight:1700;">
                    Scholarship Renewal
                </a>
                  <a href="http://127.0.0.1:8007/app/query-report/Transaction%20Report"
                   class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
                   style="margin-top:30px; font-weight:1700;">
                    Report
                </a>
                 <a href="http://127.0.0.1:8007/app/applicant-profile"
                   class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
                   style="margin-top:30px; font-weight:1700;">
                    My Profile
                </a>
                 
            </div>
        `;

        // Append custom sidebar
        if (!$(".custom-sidebar").length) {
            $("<div class='custom-sidebar mt-3'></div>")
                .html(links)
                .appendTo(frm.$wrapper.find(".layout-side-section"));
        }
        },

});

frappe.ui.form.on('Caste Percentage', {
    percentage: function(frm, cdt, cdn) {
        let total = 0;
        let seen = new Set();

        let rows = frm.doc.caste_allocate || [];

        for (let row of rows) {
            if (!row.caste_name) continue;

            let caste = row.caste_name.trim().toLowerCase();

            if (seen.has(caste)) {
                frappe.msgprint(__('Caste "{0}" is duplicated.', [row.caste_name]));
                return;
            }

            seen.add(caste);
            total += parseFloat(row.percentage || 0);
        }

        if (total > 100) {
            frappe.msgprint(__('Total percentage cannot exceed 100. Currently it is {0}.', [total]));
            frappe.model.set_value(cdt, cdn, 'percentage', 0);
        }
    },

});
