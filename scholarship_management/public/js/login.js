frappe.ready(function() {
    // Wait until login form is rendered
    let signupLink = document.createElement("a");
    signupLink.href = "/signup";   // 👉 your custom signup page route
    signupLink.innerText = "Sign up here";
    signupLink.style.cssText = "display:block; margin-top:10px; text-align:center; font-weight:bold; color:#4A90E2;";

    // Append below login button
    let loginBox = document.querySelector(".login-content .page-card-actions");
    if (loginBox) {
        loginBox.appendChild(signupLink);
    }
});
