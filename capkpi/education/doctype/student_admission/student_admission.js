// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Student Admission', {
	program: function(frm) {
		if (frm.doc.academic_year && frm.doc.program) {
			frm.doc.route = finergy.model.scrub(frm.doc.program) + "-" + finergy.model.scrub(frm.doc.academic_year)
			frm.refresh_field("route");
		}
	},

	academic_year: function(frm) {
		frm.trigger("program");
	},

	admission_end_date: function(frm) {
		if(frm.doc.admission_end_date && frm.doc.admission_end_date <= frm.doc.admission_start_date){
			frm.set_value("admission_end_date", "");
			finergy.throw(__("Admission End Date should be greater than Admission Start Date."));
		}
	}
});
