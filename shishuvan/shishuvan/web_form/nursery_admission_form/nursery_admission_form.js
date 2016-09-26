frappe.ready(function() {
	// bind events here
	$('input[name="date_of_birth"][data-doctype="Student Applicant"]').on('change', function() {
		var date = $(this).val();
		if (moment(date, moment.defaultFormat)
			< moment('2013-09-01') || moment(date, moment.defaultFormat) > moment('2014-08-30')) {
			frappe.msgprint("Child does not meet age criteria for this year's admission")
			$(this).val('');
		}
	});
});