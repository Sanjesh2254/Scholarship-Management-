frappe.listview_settings['Your Report Doctype'] = {
    onload: function(listview) {
        // Hide default sidebar
        listview.page.sidebar.empty();

        // Check role
        const is_admin = frappe.user_roles.includes('Administrator');

        const links = is_admin ? `
            <a href="/app/dashboard-view/Admin" class="btn btn-success w-100 mb-2">Dashboard</a>
            <a href="/app/scholarship" class="btn btn-success w-100 mb-2">Scholarship</a>
            <a href="/app/scholarship-application" class="btn btn-success w-100 mb-2">Application</a>
            <a href="/app/transaction" class="btn btn-success w-100 mb-2">Transaction</a>
            <a href="/app/report" class="btn btn-success w-100 mb-2">Report</a>
            <a href="/app/scholarship-settings" class="btn btn-success w-100 mb-2">Scholarship Setting</a>
        ` : `
            <a href="/app/my-dashboard" class="btn btn-success w-100 mb-2">Dashboard</a>
            <a href="/app/scholarship" class="btn btn-success w-100 mb-2">Scholarship</a>
            <a href="/app/scholarship-application" class="btn btn-success w-100 mb-2">Application</a>
            <a href="/app/scholarship-renewal" class="btn btn-success w-100 mb-2">Scholarship Renewal</a>
            <a href="/app/query-report/Transaction%20Report" class="btn btn-success w-100 mb-2">Report</a>
            <a href="/app/applicant-profile" class="btn btn-success w-100 mb-2">My Profile</a>
        `;

        // Append custom sidebar
        listview.page.sidebar.append(`<div class="custom-sidebar mt-3">${links}</div>`);
    }
};
