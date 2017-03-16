frappe.ui.form.on("Student Applicant", {
	"onload": function(frm) {
		frm.email_field = "owner";
	},
	
	refresh: function(frm) {
		if(frm.doc.application_status== "Documents Verified" && frm.doc.docstatus== 1 ) {
			frm.add_custom_button(__("Approve"), function() {
				frm.set_value("application_status", "Approved");
				frm.save_or_update();
			}, 'Actions');

			frm.add_custom_button(__("Reject"), function() {
				frm.set_value("application_status", "Rejected");
				frm.save_or_update();
			}, 'Actions');

			frm.add_custom_button(__("Wait List"), function() {
				frm.set_value("application_status", "Wait Listed");
				frm.save_or_update();
			}, 'Actions');
		}
		if(frm.doc.application_status== "Wait Listed" && frm.doc.docstatus== 1 ) {
			frm.add_custom_button(__("Approve"), function() {
				frm.set_value("application_status", "Approved");
				frm.save_or_update();

			}, 'Actions');

			frm.add_custom_button(__("Reject"), function() {
				frm.set_value("application_status", "Rejected");
				frm.save_or_update();
			}, 'Actions');
		}
	}

});
