// Copyright (c) 2025, sanjesh and contributors
// For license information, please see license.txt

frappe.ui.form.on('Scholarship Settings', {
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

    validate: function(frm) {
        let seen = new Set();
        let total = 0;

        (frm.doc.caste_allocate || []).forEach(row => {
            if (!row.caste_name) return;

            // Check duplicate caste
            let caste = row.caste_name.trim().toLowerCase();
            if (seen.has(caste)) {
                frappe.throw(__('Caste "{0}" is duplicated.', [row.caste_name]));
            }
            seen.add(caste);

            // Add percentage
            total += parseFloat(row.percentage || 0);
        });

        // Check total percentage
        if (total !== 100) {
            frappe.throw(__('Total percentage must be 100. Currently it is {0}.', [total]));
        }
    }
});

