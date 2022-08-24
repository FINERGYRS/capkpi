// Copyright (c) 2020, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('UAE VAT Settings', {
	onload: function(frm) {
		frm.set_query('account', 'uae_vat_accounts', function() {
			return {
				filters: {
					'company': frm.doc.company
				}
			};
		});
	}
});
