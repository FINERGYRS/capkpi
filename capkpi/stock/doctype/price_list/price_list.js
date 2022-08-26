// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt

finergy.ui.form.on("Price List", {
	refresh: function(frm) {
		let me = this;
		frm.add_custom_button(__("Add / Edit Prices"), function() {
			finergy.route_options = {
				"price_list": frm.doc.name
			};
			finergy.set_route("Report", "Item Price");
		}, "fa fa-money");
	}
});
