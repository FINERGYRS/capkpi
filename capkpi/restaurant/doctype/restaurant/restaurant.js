// Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Restaurant', {
	refresh: function(frm) {
		frm.add_custom_button(__('Order Entry'), () => {
			finergy.set_route('Form', 'Restaurant Order Entry');
		});
	}
});
