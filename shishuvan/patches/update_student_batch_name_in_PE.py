import frappe
from frappe.model.utils.rename_field import rename_field

def execute():

	for section in  ["KARMA", "SHRADDHA", "DHYAAN", "NEETI"]:
		if not frappe.db.exists("Student Batch Name", section):
			doc = frappe.get_doc({"doctype": "Student Batch Name", "batch_name": section})
			doc.insert()

	frappe.db.sql('''UPDATE `tabProgram Enrollment` SET student_batch_name=section''')




