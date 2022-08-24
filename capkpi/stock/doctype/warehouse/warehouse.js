// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt

finergy.ui.form.on("Warehouse", {
	setup: function (frm) {
		frm.set_query("default_in_transit_warehouse", function (doc) {
			return {
				filters: {
					warehouse_type: "Transit",
					is_group: 0,
					company: doc.company,
				},
			};
		});

		frm.set_query("parent_warehouse", function () {
			return {
				filters: {
					is_group: 1,
				},
			};
		});

		frm.set_query("account", function (doc) {
			return {
				filters: {
					is_group: 0,
					account_type: "Stock",
					company: doc.company,
				},
			};
		});
	},

	refresh: function (frm) {
		frm.toggle_display("warehouse_name", frm.doc.__islocal);
		frm.toggle_display(
			["address_html", "contact_html"],
			!frm.doc.__islocal
		);

		if (!frm.doc.__islocal) {
			finergy.contacts.render_address_and_contact(frm);
		} else {
			finergy.contacts.clear_address_and_contact(frm);
		}

		frm.add_custom_button(__("Stock Balance"), function () {
			finergy.set_route("query-report", "Stock Balance", {
				warehouse: frm.doc.name,
			});
		});

		frm.add_custom_button(
			frm.doc.is_group
				? __("Convert to Ledger", null, "Warehouse")
				: __("Convert to Group", null, "Warehouse"),
			function () {
				convert_to_group_or_ledger(frm);
			},
		);

		if (!frm.doc.is_group && frm.doc.__onload && frm.doc.__onload.account) {
			frm.add_custom_button(
				__("General Ledger", null, "Warehouse"),
				function () {
					finergy.route_options = {
						account: frm.doc.__onload.account,
						company: frm.doc.company,
					};
					finergy.set_route("query-report", "General Ledger");
				}
			);
		}

		frm.toggle_enable(["is_group", "company"], false);

		finergy.dynamic_link = {
			doc: frm.doc,
			fieldname: "name",
			doctype: "Warehouse",
		};
	},
});

function convert_to_group_or_ledger(frm) {
	finergy.call({
		method: "capkpi.stock.doctype.warehouse.warehouse.convert_to_group_or_ledger",
		args: {
			docname: frm.doc.name,
			is_group: frm.doc.is_group,
		},
		callback: function () {
			frm.refresh();
		},
	});
}
