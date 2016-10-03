from __future__ import unicode_literals

import frappe, json

def get_context(context):
	# do your magic here
	pass

def get_list_context(context):
	context.row_template = 'shishuvan/templates/includes/applicant_row.html'
	context.filters = {'program': ('!=', 'Nursery')}
