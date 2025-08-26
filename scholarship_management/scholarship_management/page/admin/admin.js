frappe.pages['admin'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Dashboard',
		single_column: true
	});


    $(page.body).append(`
        <style>
            body, html {
                margin: 0;
                padding: 0;
                height: 100%;
                overflow: hidden; /* prevent body scroll */
            }
            .admin-layout {
                display: flex;
                height: calc(100vh - 60px); /* adjust for Frappe top navbar */
                margin: 0;
            }
            #admin-sidebar {
                width: 200px;
                background: #fff;
                border-right: 1px solid #ddd;
                position: fixed;
                top: 60px; /* below Frappe header */
                left: 0;
                bottom: 0;
                padding: 20px 10px;
				
            }
            #admin-sidebar h4 {
                font-size: 14px;
                font-weight: bold;
                color: #007bff;
                margin-bottom: 20px;
                padding-left: 10px;
            }
            #admin-sidebar a {
                display: block;
                padding: 10px 15px;
                text-decoration: none;
                color: #333;
                border-radius: 6px;
                margin-bottom: 6px;
                font-size: 14px;
                transition: background 0.3s;
            }
            #admin-sidebar a:hover {
                background: #f1f1f1;
            }
            #admin-sidebar a.active {
                background: #e9f0ff;
                color: #007bff;
                font-weight: 600;
            }
            #admin-content {
                margin-left: 200px; /* push content aside */
                padding: 30px;
                height: calc(100vh - 60px);
               
            }
        </style>

        <div class="admin-layout">
            <!-- Sidebar -->
            <div id="admin-sidebar">
                <h4>Navigation</h4>
                <a href="#" class="active" data-section="dashboard">🏠 Dashboard</a>
                <a href="http://127.0.0.1:8007/app/scholarship" data-section="orders">Scholarship List</a>
                <a href="#" data-section="articles">📚 Scholarship Application</a>
                <a href="#" data-section="members">👥 Members</a>
            </div>

            <!-- Main Content -->
            <div id="admin-content">
                <h3>Welcome to the Dashboard</h3>
                <p>This is your main content area. The sidebar is fixed on the left.</p>
                <p style="margin-top: 800px;">⬇️ Scroll test: Sidebar stays fixed, only this area scrolls.</p>
            </div>
        </div>
    `);

   
};
