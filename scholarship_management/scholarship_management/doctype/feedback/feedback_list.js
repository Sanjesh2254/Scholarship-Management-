frappe.listview_settings['Feedback'] = {
    onload(listview) {
        // Clear the sidebar
        listview.page.sidebar.empty();

        // Reliable role check (no server call needed)
        const is_student =
            (frappe.user && frappe.user.has_role && frappe.user.has_role('Administrator')) ||
            ((window.frappe && Array.isArray(frappe.user_roles)) && frappe.user_roles.includes('Administrator'));

        const student_links = `
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
        `;

        const other_links = `
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
                   class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
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

        listview.page.sidebar.append(`
            <div class="custom-dashboard-link mt-3">
                ${is_student ? student_links : other_links}
            </div>
        `);
    }
};