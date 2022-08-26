// Copyright (c) 2019, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('DATEV Settings', {
	refresh: function(frm) {
		frm.add_custom_button('Show Report', () => finergy.set_route('query-report', 'DATEV'), "fa fa-table");
	}
});
