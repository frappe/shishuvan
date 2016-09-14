# -*- coding: utf-8 -*-777777yyy
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def validate_addmission_age_criteria(doc, method):
	print doc.date_of_birth
	if doc.program=="Nursery":
		if (doc.date_of_birth < "2013-09-01" or doc.date_of_birth > "2014-08-31"):
			frappe.throw("Student Applicant does not meet age criteria")