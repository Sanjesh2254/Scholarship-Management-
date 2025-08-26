frappe.pages['admin'].on_page_load = function(wrapper) {
    let page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Admin Dashboard',
        single_column: true
    });

    // Sidebar + content layout
    $(page.body).html(`
        <div class="row">
            <!-- Sidebar -->
            <div class="col-md-3">
                <div class="card shadow-sm p-3" style="height:100vh; position:sticky; top:0;">
                    <h5>📊 Dashboard Menu</h5>
                    <ul class="list-unstyled">
                        <li><a href="/app/dashboard-view/Admin">🏠 Home</a></li>
                        <li><a href="/app/scholarship">🎓 Scholarships</a></li>
                        <li><a href="/app/scholarship-renewal">🔄 Renewals</a></li>
                        <li><a href="/app/transaction">💳 Transactions</a></li>
                        <li><a href="/app/user">👤 Users</a></li>
                    </ul>
                </div>
            </div>

            <!-- Dashboard Content -->
            <div class="col-md-9" id="dashboard-content">
                <!-- Frappe will render your charts/cards here -->
            </div>
        </div>
    `);

    // Move dashboard widgets into the right section
    $('#dashboard-content').append(page.main);
};
