// Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Restaurant Menu', {
	setup: function(frm) {
		frm.add_fetch('item', 'standard_rate', 'rate');
	},
});
