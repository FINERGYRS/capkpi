// Copyright (c) 2021, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt

finergy.ui.form.on("Product Bundle", {
	refresh: function (frm) {
		frm.toggle_enable("new_item_code", frm.is_new());
		frm.set_query("new_item_code", () => {
			return {
				query: "capkpi.selling.doctype.product_bundle.product_bundle.get_new_item_code",
			};
		});
	},
});
