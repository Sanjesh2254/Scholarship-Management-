frappe.ready(function(){
    if(window.location.pathname === "/app"){
        frappe.set_route("my-dashboad")
    }
});