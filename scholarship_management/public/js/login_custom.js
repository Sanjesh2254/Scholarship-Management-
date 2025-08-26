frappe.ready(function() {
    // Wait until login form is loaded
    if (window.location.pathname === "/login") {
        let signupLink = `
            <div class="mt-3 text-center">
                <a href="/signup" style="text-decoration:none;">Create New Account</a>
            </div>
        `;
        // Append below the "Forgot Password?" link
        $(".login-content").append(signupLink);
    }
});
