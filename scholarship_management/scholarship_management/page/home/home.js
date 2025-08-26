frappe.pages['home'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Home',
        single_column: true
    });

    // Main layout with sidebar & content
    $(page.body).append(`
        <div class="row g-0">
            <!-- Sidebar -->
            <div class="col-sm-2 bg-light border-end" id="home-sidebar" style="min-height: 100vh; padding: 15px;">
                <h5 class="fw-bold mb-3">Menu</h5>
                <ul class="nav flex-column gap-2">
                    <li class="nav-item"><a class="nav-link link-dark fw-semibold" href="#" data-section="scholarships"><i class="fa fa-graduation-cap me-2"></i>Scholarships</a></li>
                    <li class="nav-item"><a class="nav-link link-dark fw-semibold" href="#" data-section="applications"><i class="fa fa-file-text me-2"></i>Applications</a></li>
                </ul>
            </div>

            <!-- Main Content -->
            <div class="col-sm-10" id="home-main-content" style="padding: 25px;">
                <h4 class="fw-bold">Welcome to the Home Page</h4>
                <p class="text-muted">Select an option from the sidebar to get started.</p>
            </div>
        </div>
    `);

    // Sidebar clicks
    $('#home-sidebar a').on('click', function(e) {
        e.preventDefault();
        let section = $(this).data('section');
        if (section === "scholarships") {
            show_scholarship_list();
        }
    });

    // Display scholarship list with cards
    function show_scholarship_list() {
        $('#home-main-content').html('<h4 class="fw-bold mb-4">Active Scholarships</h4><div class="row" id="scholarship-list"></div>');

        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Scholarship",
                fields: ["name", "eligibility_criteria", "status", "total_amount"],
                filters: { status: "Active" },
                limit_page_length: 20
            },
            callback: function(r) {
                if (r.message && r.message.length) {
                    let html = "";
                    r.message.forEach(function(row) {
                        html += `
                            <div class="col-md-4 mb-4">
                                <div class="card shadow-sm border-0 h-100">
                                    <div class="card-body d-flex flex-column">
                                        <h5 class="card-title fw-bold text-primary">${row.name}</h5>
                                        <p class="text-muted mb-2"><i class="fa fa-check-circle me-1 text-success"></i><strong>Eligibility:</strong> ${row.eligibility_criteria || "N/A"}</p>
                                        <p class="text-muted mb-2"><i class="fa fa-info-circle me-1 text-warning"></i><strong>Status:</strong> ${row.status}</p>
                                        <p class="text-muted"><i class="fa fa-money me-1 text-success"></i><strong>Amount:</strong> ${row.total_amount || "N/A"}</p>
                                        <div class="mt-auto">
                                            <button class="btn btn-sm btn-primary w-100 apply-btn" data-scholarship="${row.name}">
                                                <i class="fa fa-paper-plane me-1"></i> Apply
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `;
                    });
                    $('#scholarship-list').html(html);

                    // Apply button event
                    $('.apply-btn').on('click', function() {
                        let scholarship_name = $(this).data('scholarship');
                        apply_for_scholarship(scholarship_name);
                    });
                } else {
                    $('#scholarship-list').html('<p class="text-muted">No active scholarships found.</p>');
                }
            }
        });
    }

    // Apply for scholarship
    function apply_for_scholarship(scholarship_name) {
        frappe.call({
            method: 'scholarship_management.scholarship_management.doctype.scholarship.scholarship.get_applicant_name',
            callback: function(r) {
                if (r.message) {
                    frappe.new_doc('Scholarship Application', {
                        scholarship_name: scholarship_name,
                        applicant: r.message
                    });
                } else {
                    frappe.msgprint('Applicant not found for current user.');
                }
            }
        });
    }
};
