# -*- coding: utf-8 -*-777777yyy
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint

def validate_student_applicant(doc, method):
	validate_admission_age_criteria(doc, method)
	validate_text_size(doc, method)
	validate_milestones(doc, method)
	
def validate_admission_age_criteria(doc, method):
	if doc.program=="Nursery":
		if (doc.date_of_birth < "2013-09-01" or doc.date_of_birth > "2014-08-31"):
			frappe.throw("Student Applicant does not meet age criteria")

def validate_text_size(doc, method):
	for field in doc.meta.fields:		
		if field.fieldtype == "Text" and len(doc.get(field.fieldname)) > 1500:
			frappe.throw("{0} must be less than 300 Words (1500 Characters)".format(field.label))
	if len(doc.address_line_1) >50:
		frappe.throw("Address Line 1 cannot be greater than 50 Characters.")

def validate_milestones(doc, method):
	for field in ["held_head_steady", "could_walk_independendently", "pulled_toys_along_while_walking", 
		"could_feed_self_with_or_without_a_soppn", "recognized_the_names_of_familiar_people_object_and_body_parts",
		"spoke_word_sentences", "followed_simple_instructions", "sorted_shapes", "cooperated_with_dressing", 
		"repeated_words_spoken_to_him", "toiled_trained", "smiled_at_familiar_faces", "shared_his_toys_with_others"]:
			if cint(doc.get(field)) > 36:
				frappe.throw("{0} Milestone age cannot be greater than 36 Months".format(field))