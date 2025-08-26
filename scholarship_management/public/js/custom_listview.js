frappe.listview_settings['*'] = {
    onload: function(listview) {
        // Avoid duplicates
        if (!listview.page.sidebar.find(".custom-dashboard-link").length) {
            listview.page.sidebar.append(`
                <div class="custom-dashboard-link mt-3">
                    <a href="/app/scholarship-dashboard"
                       class="indicator-pill tag-pill tag-blue text-center w-100 d-block"
                       style="margin-top:10px; font-weight:700;">
                        📊 Dashboard
                    </a>
                </div>
            `);
        }
    }
};
