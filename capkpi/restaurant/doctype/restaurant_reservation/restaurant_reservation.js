// Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Restaurant Reservation', {
	setup: function(frm) {
		frm.add_fetch('customer', 'customer_name', 'customer_name');
	},
	refresh: function(frm) {

	}
});
