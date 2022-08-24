// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt

cur_frm.cscript.tax_table = "Purchase Taxes and Charges";

{% include "capkpi/public/js/controllers/accounts.js" %}

finergy.ui.form.on("Purchase Taxes and Charges", "add_deduct_tax", function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];

	if(!d.category && d.add_deduct_tax) {
		finergy.msgprint(__("Please select Category first"));
		d.add_deduct_tax = '';
	}
	else if(d.category != 'Total' && d.add_deduct_tax == 'Deduct') {
		finergy.msgprint(__("Cannot deduct when category is for 'Valuation' or 'Valuation and Total'"));
		d.add_deduct_tax = '';
	}
	refresh_field('add_deduct_tax', d.name, 'taxes');
});

finergy.ui.form.on("Purchase Taxes and Charges", "category", function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];

	if (d.category != 'Total' && d.add_deduct_tax == 'Deduct') {
		finergy.msgprint(__("Cannot deduct when category is for 'Valuation' or 'Vaulation and Total'"));
		d.add_deduct_tax = '';
	}
	refresh_field('add_deduct_tax', d.name, 'taxes');
});
