from __future__ import unicode_literals

import frappe

def get_context(context):
	'''Update context'''

	# make form read-only if paid
	if context.doc and context.doc.paid:
		context.read_only = 1

def get_list_context(context):
	context.row_template = 'shishuvan/templates/includes/applicant_row.html'
	context.filters = {'program': 'Nursery'}
