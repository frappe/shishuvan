# -*- coding: utf-8 -*-777777yyy
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe.utils import cint, getdate, comma_and
from dateutil.relativedelta import relativedelta
from frappe.model.mapper import get_mapped_doc


def validate_student_applicant(doc, method):
	validate_admission_age_criteria(doc, method)
	title_case_name(doc)
	validate_offline_admission(doc)
	if doc.program=="Nursery":
		validate_text_size(doc, method)
		validate_milestones(doc, method)
		validate_sibling_info(doc, method)
	else:
		doc.student_admission = "Pre-admissions for 2018-19"


def submit_student_applicant(doc, method):
	if doc.application_status != "Documents Verified":
		frappe.throw("Please change the status to 'Documents Verified' before submitting")

def validate_admission_age_criteria(doc, method):
	# only for testing purpose
	min_date = ""
	max_date = ""
	if doc.program=="Nursery":
		min_date = "2014-09-01"
		max_date = "2015-09-30"
	if doc.program=="Jr. K.G.":
		min_date = "2013-10-01"
		max_date = "2014-09-30"
	if doc.program=="Sr. K.G.":
		min_date = "2012-10-01"
		max_date = "2013-09-30"
	if doc.program=="STD. I":
		min_date = "2011-10-01"
		max_date = "2012-09-30"
	if doc.program=="STD. II":
		min_date = "2010-10-01"
		max_date = "2011-09-30"
	if doc.program=="STD. III":
		min_date = "2009-10-01"
		max_date = "2010-09-30"
	if doc.program=="STD. IV":
		min_date = "2008-10-01"
		max_date = "2009-09-30"

	if (min_date and getdate(doc.date_of_birth) < getdate(min_date) or getdate(doc.date_of_birth) > getdate(max_date)):
		frappe.throw("Child does not meet age criteria for this year's admission")

def title_case_name(doc):
	if doc.first_name:
		doc.first_name = doc.first_name.title()
	if doc.middle_name:
		doc.middle_name = doc.middle_name.title()
	if doc.last_name:
		doc.last_name = doc.last_name.title()
	if doc.title:
		doc.title = doc.title.title()

def validate_text_size(doc, method):
	for field in doc.meta.fields:
		if field.fieldtype == "Text" and len(doc.get(field.fieldname) or '') > 1500:
			frappe.throw("{0} must be less than 300 Words (1500 Characters)".format(field.label))

def validate_milestones(doc, method):
	for field in ["held_head_steady", "could_walk_independendently", "pulled_toys_along_while_walking",
		"could_feed_self_with_or_without_a_soppn", "recognized_the_names_of_familiar_people_object_and_body_parts",
		"spoke_word_sentences", "followed_simple_instructions", "sorted_shapes", "cooperated_with_dressing",
		"repeated_words_spoken_to_him", "toiled_trained", "smiled_at_familiar_faces", "shared_his_toys_with_others"]:
			if cint(doc.get(field)) > 36:
				frappe.throw("{0} milestone age cannot be greater than 36 Months".format(field))

def validate_sibling_info(doc, method):
	if doc.siblings:
		doc.number_of_siblings = len(doc.siblings)
		sibling_age = []
		for sibling in doc.siblings:
			if sibling.date_of_birth:
				sibling_age.append(relativedelta(datetime.date.today(), getdate(sibling.date_of_birth)).years)
		doc.age_of_siblings = comma_and(sibling_age)
		child_age = relativedelta(datetime.date.today(), getdate(doc.date_of_birth)).years
		if not any(age> child_age for age in sibling_age):
			doc.your_child_is_the_eldest = "Eldest"
		elif not any(age< child_age for age in sibling_age):
			doc.your_child_is_the_eldest = "Youngest"
		else:
			doc.your_child_is_the_eldest = "Middle"


def validate_offline_admission(doc):
	if doc.form_number:
		doc.paid = 1

def link_student_guardian(doc, method):
	if doc.student_applicant and not doc.guardians:
		father_guardian = get_mapped_doc("Student Applicant", doc.student_applicant,
			{"Student Applicant": {
				"doctype": "Guardian",
				"field_map": {
					"father_name": "guardian_name", 
					"father_email_id": "email_address", 
					"father_mobile_number": "mobile_number", 
					"father_landline_number": "alternate_number", 
					"father_education": "education", 
					"father_occupation": "occupation", 
					"father_work_address": "work_address", 
				}
			}}, ignore_permissions=True)
		father_guardian.save()
		doc.append("guardians", {
		"guardian": father_guardian.name,
		"guardian_name": father_guardian.guardian_name,
		"relation": "Father",
		})

		mother_guardian = get_mapped_doc("Student Applicant", doc.student_applicant,
			{"Student Applicant": {
				"doctype": "Guardian",
				"field_map": {
					"mother_name": "guardian_name", 
					"mother_email_id": "email_address", 
					"mother_mobile_number": "mobile_number", 
					"mother_landline_number": "alternate_number", 
					"mother_education": "education", 
					"mother_occupation": "occupation", 
					"mother_work_address": "work_address", 
				}
			}}, ignore_permissions=True)
		mother_guardian.save()
		doc.append("guardians", {
		"guardian": mother_guardian.name,
		"guardian_name": mother_guardian.guardian_name,
		"relation": "Mother",
		})
		doc.save()
