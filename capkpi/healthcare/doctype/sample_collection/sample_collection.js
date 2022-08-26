// Copyright (c) 2016, ESS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Sample Collection', {
	refresh: function(frm) {
		if (finergy.defaults.get_default('create_sample_collection_for_lab_test')) {
			frm.add_custom_button(__('View Lab Tests'), function() {
				finergy.route_options = {'sample': frm.doc.name};
				finergy.set_route('List', 'Lab Test');
			});
		}
	}
});

finergy.ui.form.on('Sample Collection', 'patient', function(frm) {
	if(frm.doc.patient){
		finergy.call({
			'method': 'capkpi.healthcare.doctype.patient.patient.get_patient_detail',
			args: {
				patient: frm.doc.patient
			},
			callback: function (data) {
				var age = null;
				if (data.message.dob){
					age = calculate_age(data.message.dob);
				}
				finergy.model.set_value(frm.doctype,frm.docname, 'patient_age', age);
				finergy.model.set_value(frm.doctype,frm.docname, 'patient_sex', data.message.sex);
			}
		});
	}
});

var calculate_age = function(birth) {
	var	ageMS = Date.parse(Date()) - Date.parse(birth);
	var	age = new Date();
	age.setTime(ageMS);
	var	years =  age.getFullYear() - 1970;
	return `${years} ${__('Years(s)')} ${age.getMonth()} ${__('Month(s)')} ${age.getDate()} ${__('Day(s)')}`;
};
