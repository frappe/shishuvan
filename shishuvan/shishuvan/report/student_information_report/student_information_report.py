# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []

	academic_year = filters.get("academic_year")
	program = filters.get("program")
	student_batch_name = filters.get("student_batch_name")

	columns = get_columns()
	
	program_enrollments = frappe.get_list("Program Enrollment", fields=["student", "student_name"],
		filters={"academic_year": academic_year, "program": program, "student_batch_name": student_batch_name})

	student_list = [d.student for d in program_enrollments]
	if not student_list:
		return  columns, []

	group_roll_no_map = get_student_roll_no(academic_year, program, student_batch_name)
	student_map = get_student_details(student_list)
	print (student_map)
	guardian_map = get_guardian_map(student_list)

	for d in program_enrollments:
		student_details = student_map.get(d.student)
		row = [d.student, d.student_name, group_roll_no_map.get(d.student), student_details.get("general_register_number"),\
			student_details.get("gender"), student_details.get("date_of_birth"),  student_details.get("joining_date"),\
			student_details.get("blood_group"), student_details.get("student_mobile_number"),\
			student_details.get("student_email_id"), student_details.get("address"), student_details.get("caste"),\
			student_details.get("religion"), student_details.get("nationality"), student_details.get("aadhar_number")]

		student_guardians = guardian_map.get(d.student)

		if student_guardians:
			for i in xrange(2):
				if i < len(student_guardians):
					g = student_guardians[i]
					row += [g.guardian_name, g.relation, g.mobile_number, g.email_address]
		data.append(row)

	return columns, data


def get_columns():
	columns = [
		_("Student ID") + ":Link/Student:90",
		_("Student Name") + "::150",
		_("Group Roll No") + "::60",
		_("GR Number") + "::60",
		_("Gender") + "::90",
		_("DOB") + "::90",
		_("Joining Date") + "::90",
		_("Blood Group") + "::40",
		_("Student Mobile No.") + "::110",
		_("Student Email ID") + "::125",
		_("Student Address") + "::175",
		_("Caste") + "::150",
		_("Religion") + "::150",
		_("Nationality") + "::150",
		_("AADHAR Number") + "::150",
		_("Guardian1 Name") + "::150",
		_("Relation with Guardian1") + "::80",
		_("Guardian1 Mobile No") + "::125",
		_("Guardian1 Email ID") + "::125",
		_("Guardian2 Name") + "::150",
		_("Relation with Guardian2") + "::80",
		_("Guardian2 Mobile No") + "::125",
		_("Guardian2 Email ID") + "::125",

	]
	return columns

def get_student_details(student_list):
	student_map = frappe._dict()
	student_details = frappe.db.sql('''
		select name, date_of_birth, blood_group, gender, student_mobile_number, student_email_id, address_line_1, address_line_2,
		city, state, caste, religion, nationality, general_register_number, joining_date, aadhar_number 
		from `tabStudent` where name in (%s)''' % ', '.join(['%s']*len(student_list)), tuple(student_list), as_dict=1)
	for s in student_details:
		student = frappe._dict()
		student["gender"] = s.gender
		student["date_of_birth"] = s.date_of_birth
		student["blood_group"] = s.blood_group
		student["student_mobile_number"] = s.student_mobile_number
		student["student_email_id"] = s.student_email_id
		student["address"] = ', '.join([d for d in [s.address_line_1, s.address_line_2, s.city, s.state] if d])
		student["caste"] = s.caste
		student["religion"] = s.religion
		student["nationality"] = s.nationality
		student["general_register_number"] = s.general_register_number
		student["joining_date"] = s.joining_date
		student["aadhar_number"] = s.aadhar_number
		student_map[s.name] = student
	return student_map

def get_guardian_map(student_list):
	guardian_map = frappe._dict()
	guardian_details = frappe.db.sql('''
		select  parent, guardian, guardian_name, relation  from `tabStudent Guardian` where parent in (%s)''' %
		', '.join(['%s']*len(student_list)), tuple(student_list), as_dict=1)

	guardian_list = list(set([g.guardian for g in guardian_details]))

	guardian_mobile_no = dict(frappe.db.sql("""select name, mobile_number from `tabGuardian` 
			where name in (%s)""" % ", ".join(['%s']*len(guardian_list)), tuple(guardian_list)))

	guardian_email_id = dict(frappe.db.sql("""select name, email_address from `tabGuardian` 
			where name in (%s)""" % ", ".join(['%s']*len(guardian_list)), tuple(guardian_list)))

	for guardian in guardian_details:
		guardian["mobile_number"] = guardian_mobile_no.get(guardian.guardian)
		guardian["email_address"] = guardian_email_id.get(guardian.guardian)
		guardian_map.setdefault(guardian.parent, []).append(guardian)

	return guardian_map

def get_student_roll_no(academic_year, program, batch):
	student_group = frappe.get_all("Student Group",
		filters={"academic_year":academic_year, "program":program, "batch":batch})
	if student_group:
		roll_no_dict = dict(frappe.db.sql('''select student, group_roll_number from `tabStudent Group Student` where parent=%s''',
			(student_group[0].name)))
		return roll_no_dict
	return {}
