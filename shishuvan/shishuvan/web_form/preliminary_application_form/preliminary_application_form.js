frappe.ready(function() {
	// bind events here
	function make_report_card_reqd() {
		let program = $("select[name='program'][data-doctype='Student Applicant']").val();
		if (!(in_list(["Jr. K.G.", "Sr. K.G.", "STD. I"], program))) {
			$("input[name='report_card'][data-doctype='Student Applicant']").attr("data-reqd", 1);
		} else {
			$("input[name='report_card'][data-doctype='Student Applicant']").removeAttr("data-reqd");
		}
	};
	make_report_card_reqd();
	$("select[name='program'][data-doctype='Student Applicant']").on("change", function() {
		make_report_card_reqd();
	});
})