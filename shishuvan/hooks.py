# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "shishuvan"
app_title = "Shishuvan"
app_publisher = "Frappe Technologies"
app_description = "Customization for shishuvan"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "developers@frappe.io"
app_license = "MIT"

fixtures = ["Custom Script"]

doc_events = {
	"Student Applicant": {
		"validate": "shishuvan.customization.validate_student_applicant",
		"on_submit": "shishuvan.customization.submit_student_applicant",
		"on_payment_authorized": "shishuvan.customization.on_payment_authorized"
	},
	"Student": {
		"on_update": "shishuvan.customization.link_student_guardian"
	}
}

website_context = {
	"favicon": 	'/assets/shishuvan/images/shishuvan-logo.png',
}
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/shishuvan/css/shishuvan.css"
# app_include_js = "/assets/shishuvan/js/shishuvan.js"

# include js, css files in header of web template
web_include_css = "/assets/shishuvan/css/shishuvan.css"
# web_include_js = "/assets/shishuvan/js/shishuvan.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "shishuvan.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "shishuvan.install.before_install"
# after_install = "shishuvan.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "shishuvan.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"shishuvan.tasks.all"
# 	],
# 	"daily": [
# 		"shishuvan.tasks.daily"
# 	],
# 	"hourly": [
# 		"shishuvan.tasks.hourly"
# 	],
# 	"weekly": [
# 		"shishuvan.tasks.weekly"
# 	]
# 	"monthly": [
# 		"shishuvan.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "shishuvan.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "shishuvan.event.get_events"
# }

