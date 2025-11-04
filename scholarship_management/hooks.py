app_name = "scholarship_management"
app_title = "Scholarship Management"
app_publisher = "sanjesh"
app_description = "To manage scholarship"
app_email = "sanjesh@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "scholarship_management",
# 		"logo": "/assets/scholarship_management/logo.png",
# 		"title": "Scholarship Management",
# 		"route": "/scholarship_management",
# 		"has_permission": "scholarship_management.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/scholarship_management/css/scholarship_management.css"
# app_include_js = "/assets/scholarship_management/js/scholarship_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/scholarship_management/css/scholarship_management.css"
# web_include_js = "/assets/scholarship_management/js/scholarship_management.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "scholarship_management/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "scholarship_management/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "scholarship_management.utils"
# }

# Installation
# ------------

# before_install = "scholarship_management.install.before_install"
# after_install = "scholarship_management.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "scholarship_management.uninstall.before_uninstall"
# after_uninstall = "scholarship_management.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "scholarship_management.utils.before_app_install"
# after_app_install = "scholarship_management.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "scholarship_management.utils.before_app_uninstall"
# after_app_uninstall = "scholarship_management.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "scholarship_management.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"scholarship_management.tasks.all"
# 	],
# 	"daily": [
# 		"scholarship_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"scholarship_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"scholarship_management.tasks.weekly"
# 	],
# 	"monthly": [
# 		"scholarship_management.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "scholarship_management.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "scholarship_management.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "scholarship_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["scholarship_management.utils.before_request"]
# after_request = ["scholarship_management.utils.after_request"]

# Job Events
# ----------
# before_job = ["scholarship_management.utils.before_job"]
# after_job = ["scholarship_management.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"scholarship_management.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


# permission_query_conditions = {
#     "Scholarship": "scholarship_management.scholarship_management.doctype.scholarship.scholarship.get_permission_query_conditions",
#     "Applicant Profile":"scholarship_management.scholarship_management.doctype.applicant_profile.applicant_profile.get_permission_query_conditions",
#     "Scholarship Application":"scholarship_management.scholarship_management.doctype.scholarship_application.scholarship_application.get_permission_query_conditions",
#     "Scholarship Renewal":"scholarship_management.scholarship_management.doctype.scholarship_renewal.scholarship_renewal.get_permission_query_conditions",
# }

# app_include_js =["/assets/scholarship_management/js/chat20.js",
# "/assets/scholarship_management/js/students.js",
# "https://checkout.razorpay.com/v1/approval.js"
# ],

# web_include_js = "/assets/scholarship_management/js/chat20.js"

# fixtures = [
#     {
#         "doctype": "Scholarship Add-on Type",
#         "filters": [["name", "in", [
#             "Monthly Living Stipend",
#             "Full Tuition Waiver"
#         ]]]
#     }
# ]


# scheduler_events = {
#     "cron": {
#         "0 0 * * *": [
#             "scholarship_management.scheduler.send_one_year_old_applicant_update_email",
#              "scholarship_management.scholarship_management.doctype.scholarship_application.scholarship_application.create_future_scholarships"
#         ],
#         "0 0 1 * *": [
#             "scholarship_management.sponsorship.doctype.sponsors.sponsors.send_sponsor_reminders"
#         ]
#     }
# }

permission_query_conditions = {
    "Scholarship": "scholarship_management.scholarship_management.doctype.scholarship.scholarship.get_permission_query_conditions",
    "Applicant Profile": "scholarship_management.scholarship_management.doctype.applicant_profile.applicant_profile.get_permission_query_conditions",
    "Scholarship Application": "scholarship_management.scholarship_management.doctype.scholarship_application.scholarship_application.get_permission_query_conditions",
    "Scholarship Renewal": "scholarship_management.scholarship_management.doctype.scholarship_renewal.scholarship_renewal.get_permission_query_conditions",
}

app_include_js = [
    "/assets/scholarship_management/js/chat20.js",
    "/assets/scholarship_management/js/students.js",
    "https://checkout.razorpay.com/v1/approval.js"
]

web_include_js = "/assets/scholarship_management/js/chat20.js"

fixtures = [
    {
        "doctype": "Scholarship",
    },
    {
        "doctype": "Scholarship Add-on Type",      
    },
    {
        "doctype": "Scholarship Add-on",      
    },
    {
        "doctype": "Scholarship Settings",      
    },
    {
        "doctype": "Scholarship Application",      
    },
    {
        "doctype": "Applicant Profile",      
    },
    {
        "doctype": "Scholarship Renewal",      
    },
    {
        "doctype":"Transaction"
    },
    {
        "doctype":"Sponsors"
    },
    {
        "doctype":"Feedback"
    },
    {
        "doctype":"User"
    },
    {
        "doctype":"Role"    
    },
    {
        "doctype":"Client Script"
    },
    {
        "doctype":"Workspace"
    },
    {
        "doctype":"Dashboard"
    },
    {
        "doctype":"Print Format"
    }
]



#hgadijfkffamsdkfnrtypuedi



# website_context = {
#     "favicon": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0lsq0SpUwbknMZo9ZiGP4zv_95ynllj857w&s",

#  }





