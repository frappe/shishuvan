# -*- coding: utf-8 -*-777777yyy
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, sys
import csv
from frappe.utils import getdate

def import_students():
	with open(frappe.get_app_path('shishuvan', 'students.csv')) as csvfile:
		readCSV = csv.DictReader(csvfile)
		frappe.flags.in_import = True
		i=1
		for row in readCSV:	
			sys.stdout.write("\rImporting Row {0}".format(i))
			sys.stdout.flush()
			i+=1
			student = find_student_by_name(row["Student's Name"].title(), row["Date of Birth"])
			if not student:
				student = make_student(row)	
			try:
				#enroll student
				if row["Class"] not in ["Nursery", "Jr. K.G.", "Sr. K.G.", "PS"] and row["Admission No."]:
					student.general_register_number = row["Admission No."]
					student.save()
				make_enrollment(student.name, row["Class"], row["Year"], row["Section"])
			except:
				student = make_student(row)
				student.uncertain = 1
				student.save()
				make_enrollment(student.name, row["Class"], row["Year"], row["Section"])
			frappe.db.commit()
		frappe.flags.in_import = False

def find_student_by_name(name, dob):
	student = frappe.db.get_all("Student", filters={"title": name, "date_of_birth": getdate(dob), "uncertain": 0})
	if student:
		return frappe.get_doc("Student", student[0].name)

def find_student_by_grn(grn):
	return frappe.db.get_all("Student", filters={"uncertain": 0, "general_register_number":grn})

def make_student(row):
	student = frappe.new_doc("Student")
	student.first_name = row["First Name"].title()
	student.middle_name = row["Middle Name"].title()
	student.last_name = row["Last Name"].title()
	if row["Date of Birth"]:
		student.date_of_birth = getdate(row["Date of Birth"])
	else:
		student.uncertain = 1
	student.blood_group = row["Blood Group"]
	student.gender = row["Gender"]
	student.general_register_number = row["Admission No."]
	student.address_line_1 = row["Address"][:140]
	student.city = row["City"]
	student.pincode = row["Pin Code"]
	student.student_mobile_number = row["Fax"]
	student.landline_number = row["Phone"]
	student.emergency_number = row["Emergency No."]
	student.joining_date = row["Date of Admission"]
	student.religion = row["Religion"]
	student.caste = row["Caste"]
	student.nationality = row["Nationality"]
	student.student_category = row["Student Category"]
	if find_student_by_grn(row["Admission No."]):
		student.uncertain = 1
	student.save()
	guardian = []
	if row["Mother Name"]:
		guardian.append({"guardian": make_guardian(row["Mother Name"], row["Mother Email"], \
			row["Mother Mobile"], row["Mother Organization"], row["Mother Organization Address"], \
			row["Mother Organization City"]), "relation": "Mother"})
	if row["Father Name"]:
		guardian.append({"guardian": make_guardian(row["Father Name"], row["Father Email"], \
			row["Father Mobile"], row["Father Organization"], row["Father Organization Address"], \
			row["Father Organization City"]), "relation": "Father"})
	student.set("guardians", guardian)
	student.save()
	return student

def make_guardian(name, email, mobile, org, org_address, org_city):
	guardian = frappe.new_doc("Guardian")
	guardian.guardian_name = name.title()
	guardian.email = email
	guardian.mobile = mobile
	guardian.organization = org
	guardian.work_address = org_address
	guardian.organization_city = org_city
	guardian.save()
	return guardian.name
	
def make_enrollment(student, program,academic_year, section):
	prog_enrollment = frappe.new_doc("Program Enrollment")
	prog_enrollment.student = student
	if program in ["Nursery", "Jr. K.G.", "Sr. K.G.", "PS"]:
		prog_enrollment.program = program
	else:
		prog_enrollment.program = "STD. " + program
	prog_enrollment.academic_year = academic_year
	prog_enrollment.section = section
	prog_enrollment.save()
	prog_enrollment.submit()
