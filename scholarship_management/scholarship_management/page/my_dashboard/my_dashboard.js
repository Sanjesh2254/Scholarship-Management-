frappe.pages['my-dashboard'].on_page_load = function(wrapper) {
    let page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'My Dashboard',
        single_column: false   // 👈 use false so sidebar is available
    });

    // Add content to the sidebar
    $(page.sidebar).append(`
        <div class="custom-dashboard-link mt-3">
            <a href="/app/my-dashboard"
               class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
               style="margin-top:10px; font-weight:700;">
                Dashboard
            </a>
            <a href="/app/scholarship"
               class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
               style="margin-top:30px; font-weight:700;">
                Scholarship
            </a>
            <a href="/app/scholarship-application"
               class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
               style="margin-top:30px; font-weight:700;">
                Application
            </a>
            <a href="/app/scholarship-renewal"
               class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
               style="margin-top:30px; font-weight:700;">
                Scholarship Renewal
            </a>
            <a href="/app/query-report/Transaction%20Report"
               class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
               style="margin-top:30px; font-weight:700;">
                Report
            </a>
			 <a href="/app/applicant-profile"
               class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
               style="margin-top:30px; font-weight:700;">
                My Profile
            </a>
           
        </div>
    `);
// Main content (right section)
$(page.main).html(`

<div class="col-md-12">
  <div class="p-3">

    <!-- Dashboard Cards -->
    <div class="row">
      <div class="col-md-3">
        <div class="card p-4 text-center shadow-sm" id="totalScholarshipCard" style="background:#ffd6d6; color:#b22222; border-radius:15px;">
          <h6>Available Scholarship</h6>
          <h2>0</h2>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card p-4 text-center shadow-sm" id="applicationCountCard" style="background:#d6ffd8; color:#228b22; border-radius:15px;">
          <h6>Scholarship Applied Count</h6>
          <h2>0</h2>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card p-4 text-center shadow-sm" id="scholarshipRenewalCard" style="background:#d6e0ff; color:#1e3a8a; border-radius:15px;">
          <h6>Scholarship Renewal</h6>
          <h2>0</h2>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card p-4 text-center shadow-sm" id="totalPaidCard" style="background:#fff0d6; color:#b36b00; border-radius:15px;">
          <h6>Total Approved Scholarship</h6>
          <h2>0</h2>
        </div>
      </div>
    </div>

  </div>
</div>

<script>
  function updateDashboard() {
    const user = frappe.session.user;

    // 1. Total Scholarships created by current user
    frappe.call({
      method: "frappe.client.get_list",
      args: {
        doctype: "Scholarship",
        fields: ["name"]
      },
      callback: function(r) {
        document.querySelector('#totalScholarshipCard h2').innerText = r.message.length;
      }
    });

    // 2. Applications by current user
    frappe.call({
      method: "frappe.client.get_list",
      args: {
        doctype: "Scholarship Application",
        filters: { owner: user },
        fields: ["name"]
      },
      callback: function(r) {
        document.querySelector('#applicationCountCard h2').innerText = r.message.length;
      }
    });

    // 3. Scholarship Renewals by current user
    frappe.call({
      method: "frappe.client.get_list",
      args: {
        doctype: "Scholarship Renewal",
        filters: { owner: user },
        fields: ["name"]
      },
      callback: function(r) {
        document.querySelector('#scholarshipRenewalCard h2').innerText = r.message.length;
      }
    });

    // 4. Total Paid by current user
     frappe.call({
      method: "frappe.client.get_list",
      args: {
        doctype: "Scholarship Application",
        filters: { owner: user,status: "Paid"},
        fields: ["name"]
      },
	  callback: function(r) {
        document.querySelector('#totalPaidCard h2').innerText = r.message.length;
      }
    });
  }

  // Run on page load
  updateDashboard();
</script>


    <!-- Scholarship Applications -->
    <div class="mt-5">
      <h5 class="mb-3" style="color:#1e3a8a;">Scholarship Applications</h5>

      <div class="row mb-3 g-2">
        <div class="col-md-4">
          <input type="text" id="searchName" class="form-control shadow-sm" placeholder="Search by First Letter of Name" style="border-radius:10px;">
        </div>
        <div class="col-md-4">
          <div class="btn-group w-100" role="group" id="statusFilterGroup">
            <button type="button" class="btn btn-outline-success" data-status="Paid">Paid</button>
            <button type="button" class="btn btn-outline-warning" data-status="Pending">Verified</button>
            <button type="button" class="btn btn-outline-danger" data-status="Rejected">Rejected</button>
            <button type="button" class="btn btn-outline-secondary" data-status="">All</button>
          </div>
        </div>
        <div class="col-md-4">
          <input type="date" id="searchDate" class="form-control shadow-sm" style="border-radius:10px;">
        </div>
      </div>

      <div class="table-responsive shadow-sm" style="border-radius:15px; overflow:hidden;">
        <table class="table mb-0" style="background:#f8f9fa;">
          <thead style="background:gray; color:white;">
            <tr>
              <th>S.No</th>
              <th>Scholarship Name</th>
              <th>Status</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody id="appTableBody"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<script>
  let selectedStatus = '';
  let applications = [];

  // Fetch only the current user's applications
  frappe.call({
    method: "frappe.client.get_list",
    args: {
      doctype: "Scholarship Application",
      fields: ["scholarship_name", "status", "application_date"],
      filters: { owner: frappe.session.user } // Filter by current user
    },
    callback: function(r) {
      applications = r.message;
      renderTable(applications);
    }
  });

  function renderTable(data) {
    const tbody = document.getElementById('appTableBody');
    tbody.innerHTML = "";
    data.forEach((app, index) => {
      let statusColor = "";
      if(app.status === "Paid") statusColor = "linear-gradient(45deg, #28a745, #198754)";
      else if(app.status === "Verified") statusColor = "linear-gradient(45deg, #ffc107, #e0a800)";
      else if(app.status === "Rejected") statusColor = "linear-gradient(45deg, #dc3545, #b02a37)";

      tbody.innerHTML += \`
        <tr>
          <td>\${index + 1}</td>
          <td>\${app.scholarship_name}</td>
          <td><span class="badge" style="background:\${statusColor}; color:\${app.status==="Pending"?"#000":"#fff"};">\${app.status}</span></td>
          <td>\${app.application_date}</td>
        </tr>
      \`;
    });
  }

  function filterTable() {
    let nameFilter = document.getElementById('searchName').value.toLowerCase();
    let dateFilter = document.getElementById('searchDate').value;

    let filtered = applications.filter(app => {
      let nameMatch = !nameFilter || app.scholarship_name.toLowerCase().startsWith(nameFilter);
      let statusMatch = !selectedStatus || app.status.toLowerCase() === selectedStatus.toLowerCase();
      let dateMatch = !dateFilter || app.application_date === dateFilter;
      return nameMatch && statusMatch && dateMatch;
    });

    renderTable(filtered);
  }

  document.getElementById('searchName').addEventListener('keyup', filterTable);
  document.getElementById('searchDate').addEventListener('change', filterTable);

  document.querySelectorAll('#statusFilterGroup button').forEach(btn => {
    btn.addEventListener('click', function() {
      selectedStatus = this.getAttribute('data-status');
      document.querySelectorAll('#statusFilterGroup button').forEach(b => b.classList.remove('active'));
      if(selectedStatus) this.classList.add('active');
      filterTable();
    });
  });
</script>
`);


};
